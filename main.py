import os
import click

from crewai import Agent, Crew, Process
from crewai_tools import (
    ScrapeWebsiteTool,
    GithubSearchTool,
    SerperDevTool,
)
from langchain_openai import ChatOpenAI

from modules.config import AGENTS_DEFS, TASKS_DEFS, settings
from modules.tasks import create_task

# settings env.
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = settings.SERPER_API_KEY

# setting tools
GithubSearchTools = GithubSearchTool(
    gh_token=settings.GH_TOKEN,
    github_repo=settings.GH_REPO,
    content_types=[
        "code",
    ],
)
ScrapperTools = ScrapeWebsiteTool()
SearchInternetTools = SerperDevTool()

tools = [
    SearchInternetTools,
    ScrapperTools,
    GithubSearchTools,
]


class BlogPostWriterCrew(object):
    def __init__(self):
        self.create_agents(
            llm=ChatOpenAI(
                model="gpt-4o",
                api_key=settings.OPENAI_API_KEY,
            )
        )

    def create_agents(self, llm: ChatOpenAI):
        self.senior_content_planner = Agent(
            **AGENTS_DEFS.get(settings.PLANNER),
            llm=llm,
            memory=True,
            verbose=True,
            tools=tools,
        )

        self.senior_content_writer = Agent(
            **AGENTS_DEFS.get(settings.WRITER),
            llm=llm,
            memory=True,
            verbose=True,
            tools=tools,
        )

        self.senior_content_editor = Agent(
            **AGENTS_DEFS.get(settings.EDITOR),
            llm=llm,
            memory=True,
            verbose=True,
            # tools=tools,
        )

    def run(
        self,
        topic: str,
        filename: str,
    ):
        # create tasks
        plannerTaskDef = TASKS_DEFS.get(settings.PLANNER)
        planning = create_task(
            agent=self.senior_content_planner,
            description=plannerTaskDef.get("description"),
            expected_output=plannerTaskDef.get("expected_output"),
        )

        writerTaskDef = TASKS_DEFS.get(settings.WRITER)
        writing = create_task(
            agent=self.senior_content_writer,
            description=writerTaskDef.get("description"),
            expected_output=writerTaskDef.get("expected_output"),
        )

        editorTaskDef = TASKS_DEFS.get(settings.EDITOR)
        editing = create_task(
            agent=self.senior_content_editor,
            description=editorTaskDef.get("description"),
            expected_output=editorTaskDef.get("expected_output"),
            output_file=filename,
        )

        # kickoff
        runnable = Crew(
            agents=[
                self.senior_content_planner,
                self.senior_content_writer,
                self.senior_content_editor,
            ],
            tasks=[
                planning,
                writing,
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
@click.option("--filename", required=True, type=click.STRING)
def execute(topic: str, filename: str):
    crew = BlogPostWriterCrew()
    crew.run(topic=topic, filename=filename)


if __name__ == "__main__":
    execute()
