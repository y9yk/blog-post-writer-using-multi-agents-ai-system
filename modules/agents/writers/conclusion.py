from crewai import Crew

from modules.agents import BaseAgent
from modules.config import (
    settings,
    TASKS_DEFS,
    AGENTS_DEFS,
)


class ConclusionWritingAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        #
        self.conclusion_agent_def = AGENTS_DEFS.get(settings.WRITER_FOR_CONCLUSION)
        self.conclusion_task_df = TASKS_DEFS.get(settings.WRITER_FOR_CONCLUSION)

        #
        self.agent = self._get_agent(
            **self.conclusion_agent_def,
        )

    def kickoff(self, state):
        #
        topic = state["topic"]
        research = state["research"]
        introduction = state["introduction"]
        main_text = state["main_text"]

        #
        crew = Crew(
            agents=[self.agent],
            tasks=[
                self._get_task(
                    **self.conclusion_task_df,
                    agent=self.agent,
                    callback_function=self.callback_function,
                )
            ],
        )

        result = crew.kickoff(
            inputs={
                "topic": topic,
                "research_output": research,
                "introduction_output": introduction,
                "main_text_output": main_text,
            }
        )

        # store state and return
        state["conclusion"] = result
        return {
            **state,
        }
