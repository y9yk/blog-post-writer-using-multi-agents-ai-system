from duckduckgo_search import DDGS

from blog_poster.retriever.providers import BaseRetriever
from config import settings


class Duckduckgo(BaseRetriever):
    """
    Duckduckgo API Retriever
    """

    def __init__(self):
        super().__init__()
        self.ddg = DDGS()

    def search(
        self,
        query: str,
        max_results=settings.MAX_RESULTS,
    ):
        """
        Performs the search
        :param query:
        :param max_results:
        :return:
        """
        ddgs_gen = self.ddg.text(
            query,
            region="kr-kr",
            max_results=max_results,
        )
        return ddgs_gen
