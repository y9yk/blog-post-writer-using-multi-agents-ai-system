from crewai import Crew
from crewai_tools import ScrapeWebsiteTool

from modules.agents import BaseAgent
from modules.config import (
    settings,
    TASKS_DEFS,
    AGENTS_DEFS,
)


class IntroductionWritingAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        #
        self.introduction_agent_def = AGENTS_DEFS.get(settings.WRITER_FOR_INTRODUCTION)
        self.introduction_task_df = TASKS_DEFS.get(settings.WRITER_FOR_INTRODUCTION)

        #
        self.agent = self._get_agent(
            **self.introduction_agent_def,
            tools=[
                ScrapeWebsiteTool(),
            ],
        )

    def kickoff(self, state):
        #
        topic = state["topic"]
        research = state["research"]

        #
        crew = Crew(
            agents=[self.agent],
            tasks=[
                self._get_task(
                    **self.introduction_task_df,
                    agent=self.agent,
                    callback_function=self.callback_function,
                )
            ],
        )

        result = crew.kickoff(
            inputs={
                "topic": topic,
                "research_output": research,
            }
        )

        # store state and return
        state["introduction"] = result
        return {
            **state,
        }
