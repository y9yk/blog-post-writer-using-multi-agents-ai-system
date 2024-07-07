import os
import click

from crewai import Agent, Crew, Process
from crewai_tools import (
    ScrapeWebsiteTool,
    GithubSearchTool,
)
from langchain_openai import ChatOpenAI

from modules.config import AGENTS_DEFS, TASKS_DEFS, settings
from modules.tasks import create_task

# settings env.
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = settings.SERPER_API_KEY

# setting tools
website_scrape_tool = ScrapeWebsiteTool()
github_search_tool = GithubSearchTool(
    gh_token=settings.GH_TOKEN,
    github_repo=settings.GH_REPO,
    content_types=[
        "code",
    ],
)


class BlogPostWriterCrew(object):
    def __init__(self):
        self.create_agents(
            llm=ChatOpenAI(
                model=settings.OPENAI_MODEL_NAME,
                api_key=settings.OPENAI_API_KEY,
            )
        )

    def create_agents(self, llm: ChatOpenAI):
        self.senior_content_researcher = Agent(
            **AGENTS_DEFS.get(settings.RESEARCHER),
            llm=llm,
            memory=True,
            verbose=True,
            tools=[website_scrape_tool],
        )

        self.senior_content_writer_for_introduction = Agent(
            **AGENTS_DEFS.get(settings.WRITER_FOR_INTRODUCTION),
            llm=llm,
            memory=True,
            verbose=True,
            tools=[website_scrape_tool],
        )

        self.senior_content_writer_for_main_text = Agent(
            **AGENTS_DEFS.get(settings.WRITER_FOR_MAIN_TEXT),
            llm=llm,
            memory=True,
            verbose=True,
            tools=[website_scrape_tool],
        )

        self.senior_content_writer_for_conclusion = Agent(
            **AGENTS_DEFS.get(settings.WRITER_FOR_CONCLUSION),
            llm=llm,
            memory=True,
            verbose=True,
            tools=[website_scrape_tool],
        )

        self.senior_content_writer_for_code = Agent(
            **AGENTS_DEFS.get(settings.WRITER_FOR_CODE),
            llm=llm,
            memory=True,
            verbose=True,
            tools=[
                website_scrape_tool,
                github_search_tool,
            ],
        )

        self.senior_content_editor = Agent(
            **AGENTS_DEFS.get(settings.EDITOR),
            llm=llm,
            memory=True,
            verbose=True,
            tools=[website_scrape_tool],
        )

    def run(
        self,
        topic: str,
    ):
        # create tasks
        researchTaskDef = TASKS_DEFS.get(settings.RESEARCHER)
        research = create_task(
            agent=self.senior_content_researcher,
            description=researchTaskDef.get("description"),
            expected_output=researchTaskDef.get("expected_output"),
            output_file=settings.OUTPUT_RESEARCH,
        )

        writerIntroTaskDef = TASKS_DEFS.get(settings.WRITER_FOR_INTRODUCTION)
        introduction = create_task(
            agent=self.senior_content_writer_for_introduction,
            description=writerIntroTaskDef.get("description"),
            expected_output=writerIntroTaskDef.get("expected_output"),
            output_file=settings.OUTPUT_INTRODUCTION,
        )

        writerMainTaskDef = TASKS_DEFS.get(settings.WRITER_FOR_MAIN_TEXT)
        main_text = create_task(
            agent=self.senior_content_writer_for_main_text,
            description=writerMainTaskDef.get("description"),
            expected_output=writerMainTaskDef.get("expected_output"),
            output_file=settings.OUTPUT_MAIN_TEXT,
        )

        writerConclusionTaskDef = TASKS_DEFS.get(settings.WRITER_FOR_CONCLUSION)
        conclusion = create_task(
            agent=self.senior_content_writer_for_conclusion,
            description=writerConclusionTaskDef.get("description"),
            expected_output=writerConclusionTaskDef.get("expected_output"),
            output_file=settings.OUTPUT_CONCLUSION,
        )

        writerCodeTaskDef = TASKS_DEFS.get(settings.WRITER_FOR_CODE)
        code = create_task(
            agent=self.senior_content_writer_for_code,
            description=writerCodeTaskDef.get("description"),
            expected_output=writerCodeTaskDef.get("expected_output"),
            output_file=settings.OUTPUT_CODE,
        )

        editorTaskDef = TASKS_DEFS.get(settings.EDITOR)
        editing = create_task(
            agent=self.senior_content_editor,
            description=editorTaskDef.get("description"),
            expected_output=editorTaskDef.get("expected_output"),
            output_file=settings.EDITOR,
        )

        # kickoff
        runnable = Crew(
            agents=[
                self.senior_content_researcher,
                self.senior_content_writer_for_introduction,
                self.senior_content_writer_for_main_text,
                self.senior_content_writer_for_conclusion,
                self.senior_content_writer_for_code,
                self.senior_content_editor,
            ],
            tasks=[
                research,
                introduction,
                main_text,
                conclusion,
                code,
                editing,
            ],
            process=Process.sequential,
            verbose=True,
        )
        return runnable.kickoff(
            inputs={
                "topic": topic,
            }
        )


@click.command()
@click.option("--topic", required=True, type=click.STRING)
def execute(topic: str):
    crew = BlogPostWriterCrew()
    crew.run(topic=topic)


if __name__ == "__main__":
    execute()
