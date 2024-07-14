import abc
from typing import List

from fastapi import WebSocket

from blog_poster.exceptions import NotImplementedException
from blog_poster.utils import Tone, logger


class BaseAgent(object):
    __metaclass__ = abc.ABCMeta

    def __init__(
        self,
        query: str,
        parent_query: str = None,
        tone: Tone = Tone.Objective.value,
        agent_name: str = None,
        agent_role: str = None,
        context: List = [],
        visited_urls: List = [],
        verbose: bool = False,
        websocket: WebSocket = None,
    ):
        logger.debug(locals())

        # define vars.
        self.query = query
        self.parent_query = parent_query
        self.tone = tone
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.context = context
        self.visited_urls = visited_urls

        # for logging
        self.verbose = verbose
        self.websocket = websocket

        # calculate costs
        self.costs: float = 0.0

    def get_visited_urls(self) -> list:
        return list(self.visited_urls)

    def get_context(self) -> list:
        return self.context

    def get_costs(self) -> float:
        return self.costs

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def add_costs(self, cost: int) -> None:
        self.costs += cost

    @abc.abstractmethod
    def run(self):
        raise NotImplementedException()
