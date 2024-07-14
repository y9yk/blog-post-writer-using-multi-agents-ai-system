from blog_poster.config import settings
from blog_poster.exceptions import NotImplementedException


def get_embeddings(embedding_provider, **kwargs):
    match embedding_provider:
        case "openai":
            from langchain_openai import OpenAIEmbeddings

            _embeddings = OpenAIEmbeddings(
                model=settings.OPENAI_EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_API_BASE,
                check_embedding_ctx_length=False,
            )
        case "sentence":
            from .providers import SentenceEmbeddings

            _embeddings = SentenceEmbeddings()
        case _:
            raise NotImplementedException()

    return _embeddings
