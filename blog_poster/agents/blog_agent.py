import asyncio
import json

import json_repair
from fastapi import WebSocket
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.embeddings import Embeddings

from blog_poster.agents import BaseAgent
from blog_poster.agents.schema import Subtopics
from blog_poster.config import settings
from blog_poster.context import ContextCompressor
from blog_poster.embedding import get_embeddings
from blog_poster.llm import create_chat_completion, get_llm
from blog_poster.prompts import (
    auto_agent_instructions,
    generate_report_introduction,
    generate_search_queries_prompt,
    generate_subtopic_report_prompt,
    generate_subtopics_prompt,
)
from blog_poster.retriever import BaseRetriever, get_retriever
from blog_poster.scraper import Scraper
from blog_poster.utils import handle_json_error, logger, stream_output


class BlogAgent(BaseAgent):
    """
    Blog Agent
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #
        self.retreiver: BaseRetriever = get_retriever(settings.RETRIEVER_TYPE)
        self.embeddings: Embeddings = get_embeddings(settings.EMBEDDINGS_TYPE)

    async def _get_similar_content_by_query(
        self,
        query: str,
        documents,
        websocket: WebSocket = None,
    ):
        if self.verbose:
            await stream_output(
                "logs",
                f"📝 Getting relevant content based on query: {query}",
                websocket=websocket,
            )

        # summarize raw data
        context_compressor = ContextCompressor(
            documents=documents, embeddings=self.embeddings
        )

        return context_compressor.get_context(
            query=query,
            max_results=settings.MAX_RESULTS,
        )

    def _get_scraped_contents_from_url(self, urls):
        contents = []
        try:
            # scrape content
            contents = Scraper(
                urls,
                settings.USER_AGENT,
                settings.SCRAPER_TYPE,
            ).run()
        except Exception as e:
            logger.error(f"Error in scrape_urls: {e}")
        return contents

    async def _get_urls_from_search_results(
        self,
        search_urls,
    ):
        new_urls = []
        for url in search_urls:
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                new_urls.append(url)
                if settings.DEBUG:
                    await stream_output(
                        "logs",
                        f"✅ Added source url to research: {url}\n",
                        websocket=self.websocket,
                    )

        return new_urls

    async def _get_agent_info(self):
        query = (
            f"{self.parent_query} - {self.query}"
            if self.parent_query
            else f"{self.query}"
        )
        response = None

        try:
            response = await create_chat_completion(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": f"{auto_agent_instructions()}"},
                    {"role": "user", "content": f"task: {query}"},
                ],
                temperature=0,
                llm_provider=settings.LLM_TYPE,
                cost_callback=self.add_costs,
            )

            agent_dict = json.loads(response)
            return agent_dict["server"], agent_dict["agent_role_prompt"]

        except:
            logger.debug("⚠️ Error in reading JSON, attempting to repair JSON")
            return await handle_json_error(response)

    async def _get_sub_quries(self):
        response = await create_chat_completion(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": f"{self.agent_role}"},
                {
                    "role": "user",
                    "content": generate_search_queries_prompt(
                        query=self.query,
                        parent_query=self.parent_query,
                        max_sub_queries=settings.MAX_SUB_QUERIES,
                    ),
                },
            ],
            temperature=0,
            llm_provider=settings.LLM_TYPE,
            cost_callback=self.add_costs,
        )

        sub_queries = json_repair.loads(response)

        return sub_queries

    async def _process_sub_query(self, sub_query: str):
        if self.verbose:
            await stream_output(
                "logs",
                f"Running research for {sub_query}",
                self.websocket,
            )

        # search urls
        search_results = self.retreiver.search(query=sub_query)
        search_urls = await self._get_urls_from_search_results(
            [url.get("href") for url in search_results]
        )

        # scrape contents from urls
        contents = self._get_scraped_contents_from_url(urls=search_urls)
        contents = await self._get_similar_content_by_query(
            query=sub_query,
            documents=contents,
        )
        if self.verbose:
            if contents:
                await stream_output(
                    "logs",
                    f"{contents}",
                    self.websocket,
                )
            else:
                await stream_output(
                    "logs",
                    f"No contents for {sub_query}",
                    self.websocket,
                )

        return contents

    async def _get_subtopics(self):
        try:
            parser = PydanticOutputParser(pydantic_object=Subtopics)

            prompt = PromptTemplate(
                template=generate_subtopics_prompt(),
                input_variables=["task", "data", "subtopics", "max_subtopics"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )

            provider = get_llm(llm_provider=settings.LLM_TYPE)
            model = provider.llm

            chain = prompt | model | parser

            output = chain.invoke(
                {
                    "task": self.query,
                    "data": self.context,
                    "subtopics": [],
                    "max_subtopics": settings.MAX_SUB_TOPICS,
                }
            )

            return output
        except Exception as e:
            logger.error("Exception in parsing subtopics : ", e)
            return []

    async def _generate_introduction(self):
        try:
            introduction = await create_chat_completion(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": f"{self.agent_role}"},
                    {
                        "role": "user",
                        "content": generate_report_introduction(
                            self.query,
                            self.context,
                        ),
                    },
                ],
                temperature=0,
                llm_provider=settings.LLM_TYPE,
                stream=True,
                websocket=self.websocket,
                cost_callback=self.add_costs,
            )

            return introduction
        except Exception as e:
            logger.error(f"Error in generating report introduction: {e}")
        return ""

    async def _generate_subtopic_report(
        self,
        existing_headers: list = [],
    ):
        report = ""
        content = generate_subtopic_report_prompt(
            current_subtopic=self.query,
            existing_headers=existing_headers,
            main_topic=self.parent_query,
            context=self.context,
            total_words=settings.TOTAL_WORDS_IN_SECTION,
        )

        try:
            report = await create_chat_completion(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": f"{self.agent_role}"},
                    {"role": "user", "content": content},
                ],
                temperature=0,
                llm_provider=settings.LLM_TYPE,
                stream=True,
                websocket=self.websocket,
                cost_callback=self.add_costs,
            )
        except Exception as e:
            logger.error(f"Error in generate_report: {e}")

        return report

    ##################################################
    # Tasks
    # - 1) initial_research
    # - 2) generate_subtopics
    # - 3) generate_introduction
    # - 4) generate_subtopic_reports (research & write_report) -> processor
    # - 5) construct_detail_report -> processor
    ##################################################

    async def research(self):
        # reset visited_urls
        self.visited_urls.clear()

        # generate agent
        if not (self.agent_name and self.agent_role):
            self.agent_name, self.agent_role = await self._get_agent_info()

        if self.verbose:
            await stream_output(
                "logs",
                f"Starting the research task for {self.query}",
                self.websocket,
            )

        # processing
        sub_queries = await self._get_sub_quries()
        sub_queries.append(self.query)

        if self.verbose:
            await stream_output(
                "logs",
                f"Conduct research based on the following queries: {sub_queries}",
                self.websocket,
            )

        self.context = await asyncio.gather(
            *[self._process_sub_query(sub_query=sub_query) for sub_query in sub_queries]
        )

        if self.verbose:
            await stream_output(
                "logs",
                f"Total Research Costs: ${self.get_costs()}",
                self.websocket,
            )

        return self.context

    async def generate_subtopics(self):
        if self.verbose:
            await stream_output(
                "logs",
                f"Generating subtopics",
                self.websocket,
            )

        subtopics = await self._get_subtopics()

        if self.verbose:
            await stream_output(
                "logs",
                f"Subtopics: {subtopics}",
                self.websocket,
            )

        return subtopics

    async def generate_introduction(self):
        return self._generate_introduction(self)

    async def generate_subtopic_report(self, existing_headers: list = []):
        if self.verbose:
            await stream_output(
                "logs",
                f"Writing subtopic report: {self.query}",
                self.websocket,
            )

        report = self._generate_subtopic_report(existing_headers=existing_headers)
        return report
