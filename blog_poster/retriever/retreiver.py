from blog_poster.exceptions import NotImplementedException
from blog_poster.retriever.providers import BaseRetriever


def get_retriever(retriever) -> BaseRetriever:
    """
    Gets the retriever
    Args:
        retriever: retriever name

    Returns:
        retriever: Retriever class

    """
    match retriever:
        case "duckduckgo":
            from blog_poster.retriever.providers import Duckduckgo as Retriever

        case _:
            raise NotImplementedException

    retriever = Retriever()
    return retriever
