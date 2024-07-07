import os
import click

from langgraph.graph import END, StateGraph

from modules.config import settings
from modules.graph import BlogTaskGraphState
from modules.agents import (
    ResearchAgent,
    IntroductionWritingAgent,
    MainTextWritingAgent,
    ConclusionWritingAgent,
    EditorAgent,
)

# settings env.
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


class BlogPostWriter(object):
    def __init__(self):
        self.workflow = StateGraph(BlogTaskGraphState)

    def run(
        self,
        topic: str,
    ):
        # register node
        self.workflow.add_node(settings.RESEARCHER, ResearchAgent().kickoff)
        self.workflow.add_node(
            settings.WRITER_FOR_INTRODUCTION, IntroductionWritingAgent().kickoff
        )
        self.workflow.add_node(
            settings.WRITER_FOR_MAIN_TEXT, MainTextWritingAgent().kickoff
        )
        self.workflow.add_node(
            settings.WRITER_FOR_CONCLUSION, ConclusionWritingAgent().kickoff
        )

        # register edge
        self.workflow.set_entry_point(settings.RESEARCHER)
        self.workflow.add_edge(settings.RESEARCHER, settings.WRITER_FOR_INTRODUCTION)
        self.workflow.add_edge(
            settings.WRITER_FOR_INTRODUCTION, settings.WRITER_FOR_MAIN_TEXT
        )
        self.workflow.add_edge(
            settings.WRITER_FOR_MAIN_TEXT, settings.WRITER_FOR_CONCLUSION
        )
        self.workflow.add_edge(settings.WRITER_FOR_CONCLUSION, END)

        # compile
        pipeline = self.workflow.compile()
        for output in pipeline.stream({"topic": topic}):
            print(output)


@click.command()
@click.option("--topic", required=True, type=click.STRING)
def execute(topic: str):
    processor = BlogPostWriter()
    processor.run(topic=topic)


if __name__ == "__main__":
    execute()
