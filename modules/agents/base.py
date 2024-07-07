import abc
import logging
from textwrap import dedent
from typing import Callable, List

from crewai import Agent, Task
from crewai.task import TaskOutput
from langchain_openai import ChatOpenAI

from modules.config import settings
from modules.exceptions import NotImplementedException


class BaseAgent(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
        )

        #
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    def _get_agent(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: List = [],
        allow_delegation: bool = False,
        memory: bool = True,
        verbose: bool = True,
    ) -> Agent:
        """
        create an agent and return
        """
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            allow_delegation=allow_delegation,
            llm=self.llm,
            memory=memory,
            verbose=verbose,
        )

    def _get_task(
        self,
        agent: Agent,
        description: str,
        expected_output: str,
        async_execution: bool = False,
        output_file: str = None,
        callback_function: Callable = None,
    ) -> Task:
        """
        create a task and return
        """
        task = Task(
            agent=agent,
            description=dedent(description),
            expected_output=dedent(expected_output),
            async_execution=async_execution,
            callback=callback_function,
            output_file=output_file,
        )
        return task

    def callback_function(self, output: TaskOutput):
        self.logger.debug(output.raw_output)

    @abc.abstractmethod
    def kickoff(self, state):
        raise NotImplementedException()
