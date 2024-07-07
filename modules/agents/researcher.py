from crewai import Crew
from crewai_tools import ScrapeWebsiteTool

from modules.agents import BaseAgent
from modules.config import (
    settings,
    TASKS_DEFS,
    AGENTS_DEFS,
)


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        #
        self.research_agent_def = AGENTS_DEFS.get(settings.RESEARCHER)
        self.research_task_df = TASKS_DEFS.get(settings.RESEARCHER)

        #
        self.agent = self._get_agent(
            **self.research_agent_def,
            tools=[
                ScrapeWebsiteTool(),
            ],
        )

    def kickoff(self, state):
        #
        topic = state["topic"]

        #
        crew = Crew(
            agents=[self.agent],
            tasks=[
                self._get_task(
                    **self.research_task_df,
                    agent=self.agent,
                    callback_function=self.callback_function,
                )
            ],
        )

        result = crew.kickoff(
            inputs={
                "topic": topic,
            }
        )

        # store state and return
        state["research"] = result
        return {
            **state,
        }
