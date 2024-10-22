import os

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import (
    DocumentCompressorPipeline,
    EmbeddingsFilter,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

from blog_poster.context.retriever import DocumentRetreiver


class ContextCompressor:
    def __init__(self, documents, embeddings, max_results=5, **kwargs):
        self.max_results = max_results
        self.documents = documents
        self.kwargs = kwargs
        self.embeddings = embeddings
        self.similarity_threshold = os.environ.get("SIMILARITY_THRESHOLD", 0.38)

    def __get_contextual_retriever(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        relevance_filter = EmbeddingsFilter(embeddings=self.embeddings, similarity_threshold=self.similarity_threshold)
        pipeline_compressor = DocumentCompressorPipeline(transformers=[splitter, relevance_filter])
        base_retriever = DocumentRetreiver(pages=self.documents)
        contextual_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=base_retriever
        )
        return contextual_retriever

    def __pretty_print_docs(self, docs, top_n):
        return f"\n".join(
            f"Source: {d.metadata.get('source')}\n" f"Title: {d.metadata.get('title')}\n" f"Content: {d.page_content}\n"
            for i, d in enumerate(docs)
            if i < top_n
        )

    def get_context(self, query, max_results=5):
        compressed_docs = self.__get_contextual_retriever()
        relevant_docs = compressed_docs.invoke(query)
        return self.__pretty_print_docs(relevant_docs, max_results)
