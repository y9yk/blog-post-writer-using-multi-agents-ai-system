import os
from datetime import datetime
from functools import lru_cache
from os import path
from typing import Dict

from pydantic_settings import BaseSettings
from pytz import timezone


class Settings(BaseSettings):
    """
    기본 Configuration
    """

    PROJECT_ROOT: str = path.dirname(
        path.dirname(
            path.dirname(
                (path.abspath(__file__)),
            ),
        )
    )

    PROJECT_NAME: str = "blog_poster"
    PROJECT_DESC: str = ""

    DEBUG: bool = True

    # service
    API_PREFIX: str = "/blog_poster/api"
    API_HC_PREFIX: str = f"/blog_poster"

    # db
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_NAME: str = "blog_poster"
    DB_PORT: int = 3306
    DB_ECHO: bool = True
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_PRE_PING: bool = True

    # openai
    OPENAI_MODEL_NAME: str = ""
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = ""
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # openai cost
    # Per OpenAI Pricing Page: https://openai.com/api/pricing/
    ENCODING_MODEL: str = "o200k_base"
    INPUT_COST_PER_TOKEN: float = 0.000005
    OUTPUT_COST_PER_TOKEN: float = 0.000015
    IMAGE_INFERENCE_COST: float = 0.003825
    EMBEDDING_COST: float = 0.02 / 1000000  # Assumes new ada-3-small

    # embedding
    EMBEDDING_MODEL_PATH: str = f"{PROJECT_ROOT}/resources/embeddings"

    # retriever and scraper, embedding type
    RETRIEVER_TYPE: str = "duckduckgo"
    SCRAPER_TYPE: str = "web_base_loader"
    LLM_TYPE: str = "openai"
    # EMBEDDINGS_TYPE: str = "sentence"
    EMBEDDINGS_TYPE: str = "openai"

    #
    MAX_RESULTS: int = 10
    MAX_SUB_QUERIES: int = 5
    MAX_SUB_TOPICS: int = 5
    MAX_SUB_SECTIONS: int = 5
    TOTAL_WORDS_IN_SECTION: int = 3000

    # user-agent
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"

    CURRENT_DT: str = datetime.now(timezone("Asia/Seoul")).strftime("%Y%m%d")

    # langfuse integration
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = ""

    class Config:
        env_prefix = ""
        env_file = [f"{os.path.dirname(os.path.abspath(__file__))}/{file_name}" for file_name in [".env"]]
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
