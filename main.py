import asyncio

import click
from fastapi import WebSocket

from blog_poster.agents import BlogAgent
from blog_poster.agents.schema import Subtopics
from blog_poster.utils import add_source_urls, extract_headers, table_of_contents


class Processor(object):
    def __init__(
        self,
        query: str,
        verbose: bool = False,
        websocket: WebSocket = None,
    ):
        #
        self.query = query
        self.verbose = verbose
        self.websocket = websocket

        self.global_urls = []
        self.global_context = []
        self.existing_headers = []

        #
        self.main_agent = BlogAgent(
            query=query,
            verbose=verbose,
            websocket=websocket,
        )

    async def _process_sub_topics(
        self,
        subtopic: str,
        verbose: bool = False,
        websocket: WebSocket = None,
    ):
        # create subtopic agent
        self.subtopic_agent = BlogAgent(
            query=subtopic,
            parent_query=self.query,
            agent_name=self.main_agent.agent_name,
            agent_role=self.main_agent.agent_role,
            context=self.global_context,
            visited_urls=self.global_urls,
            verbose=verbose,
            websocket=websocket,
        )

        # research -> write_report
        await self.subtopic_agent.research()
        report_body = await self.subtopic_agent.generate_subtopic_report(existing_headers=self.existing_headers)

        # store context, visited_urls
        self.global_context.extend(self.subtopic_agent.context)
        self.global_urls.extend(self.subtopic_agent.visited_urls)

        # update existing headers
        self.existing_headers.append({"subtopic task": subtopic, "headers": extract_headers(report_body)})

        return report_body

    def _finalize(self, introduction: str, report_body: str):
        # create table of contents
        toc = table_of_contents(report_body)

        #
        report_with_references = add_source_urls(
            report_body,
            self.global_urls,
        )

        return f"{introduction}\n\n{toc}\n\n{report_with_references}"

    async def run(self):
        # step 1) research and generate subtopics
        await self.main_agent.research()
        generated_subtopics: Subtopics = await self.main_agent.generate_subtopics()

        #
        self.global_context.extend(self.main_agent.context)
        self.global_urls.extend(self.main_agent.visited_urls)

        # write introduction
        introduction = await self.main_agent.generate_introduction()

        # process subtopics
        report_body = []
        for subtopic in generated_subtopics.subtopics:
            report_body.append(
                await self._process_sub_topics(
                    subtopic=subtopic.task,
                    verbose=self.verbose,
                    websocket=self.websocket,
                )
            )
        report_body = "\n\n\n".join(report_body)

        # finalize
        return self._finalize(
            introduction=introduction,
            report_body=report_body,
        )


@click.command()
@click.option("--query", required=True, type=click.STRING)
@click.option(
    "--verbose",
    required=False,
    type=click.BOOL,
    default=False,
)
def execute(query: str, verbose: bool):
    # create event loop
    loop = asyncio.get_event_loop()

    processor = Processor(query=query, verbose=verbose)
    loop.run_until_complete(processor.run())

    # close event loop
    loop.close()


if __name__ == "__main__":
    execute()
