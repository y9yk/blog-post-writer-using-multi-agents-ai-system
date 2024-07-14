from typing import List

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from blog_poster.config import settings


class SentenceEmbeddings(Embeddings):
    def __init__(self):
        # load model
        self.model = SentenceTransformer(
            model_name_or_path=settings.EMBEDDING_MODEL_PATH
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        assert all(
            bool(text) and isinstance(text, str) for text in texts
        ), "submit a list of non-empty strings"

        ret = []
        for text in texts:
            output = self.model.encode(text, normalize_embedding=True)
            ret.append(output.tolist())
        return ret

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        assert bool(text) and isinstance(text, str), "submit a non-empty string"

        output = self.model.encode(text, normalize_embeddings=True)
        return output.tolist()
