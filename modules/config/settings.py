import os
from functools import lru_cache
from os import path
from typing import Dict

from pydantic_settings import BaseSettings


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

    PROJECT_NAME: str = "crew"
    PROJECT_DESC: str = ""

    DEBUG: bool = True

    # project
    OPENAI_API_KEY: str = ""
    SERPER_API_KEY: str = ""
    GH_TOKEN: str = ""
    GH_REPO: str = ""

    # workers
    PLANNER: str = "senior_content_planner"
    WRITER: str = "senior_content_writer"
    EDITOR: str = "senior_content_editor"

    class Config:
        env_prefix = ""
        env_file = [
            f"{os.path.dirname(os.path.abspath(__file__))}/{file_name}"
            for file_name in [".env"]
        ]
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
