from crewai import Crew, Process
from crewai_tools import ScrapeWebsiteTool, GithubSearchTool

from modules.agents import BaseAgent
from modules.config import (
    settings,
    TASKS_DEFS,
    AGENTS_DEFS,
)


class MainTextWritingAgent(BaseAgent):

    def __init__(self):
        super().__init__()

        #
        self.main_text_agent_def = AGENTS_DEFS.get(settings.WRITER_FOR_MAIN_TEXT)
        self.code_agent_def = AGENTS_DEFS.get(settings.WRITER_FOR_CODE)

        self.main_text_task_df = TASKS_DEFS.get(settings.WRITER_FOR_MAIN_TEXT)
        self.code_task_df = TASKS_DEFS.get(settings.WRITER_FOR_CODE)

        #
        self.main_text_agent = self._get_agent(
            **self.main_text_agent_def,
            tools=[
                ScrapeWebsiteTool(),
            ],
        )
        self.code_agent = self._get_agent(
            **self.code_agent_def,
            tools=[
                GithubSearchTool(
                    gh_token=settings.GH_TOKEN,
                    github_repo=settings.GH_REPO,
                    content_types=[
                        "code",
                    ],
                )
            ],
        )

    def kickoff(self, state):
        #
        topic = state["topic"]
        research = state["research"]
        introduction = state["introduction"]

        #
        crew = Crew(
            agents=[
                self.main_text_agent,
                self.code_agent,
            ],
            tasks=[
                self._get_task(
                    **self.main_text_task_df,
                    agent=self.main_text_agent,
                    callback_function=self.callback_function,
                ),
                self._get_task(
                    **self.code_task_df,
                    agent=self.code_agent,
                    callback_function=self.callback_function,
                ),
            ],
            process=Process.sequential,
        )

        result = crew.kickoff(
            inputs={
                "topic": topic,
                "research_output": research,
                "introduction_output": introduction,
            }
        )

        # store state and return
        state["main_text"] = result
        return {
            **state,
        }
