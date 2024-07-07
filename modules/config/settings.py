import os
from functools import lru_cache
from os import path
from typing import Dict
from datetime import datetime
from pytz import timezone

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
    OPENAI_MODEL_NAME: str = ""
    OPENAI_API_KEY: str = ""
    SERPER_API_KEY: str = ""
    GH_TOKEN: str = ""
    GH_REPO: str = ""

    # workers
    RESEARCHER: str = "senior_content_researcher"
    WRITER_FOR_INTRODUCTION: str = "senior_content_writer_for_introduction"
    WRITER_FOR_MAIN_TEXT: str = "senior_content_writer_for_main_text"
    WRITER_FOR_CONCLUSION: str = "senior_content_writer_for_conclusion"
    WRITER_FOR_CODE: str = "senior_content_writer_for_code"
    EDITOR: str = "senior_content_editor"

    # output files
    CURRENT_DT: str = datetime.now(timezone("Asia/Seoul")).strftime("%Y%m%d")
    OUTPUT_FILEPATH: str = f"{PROJECT_ROOT}/resources/{CURRENT_DT}"
    OUTPUT_RESEARCH: str = f"{OUTPUT_FILEPATH}/research.md"
    OUTPUT_INTRODUCTION: str = f"{OUTPUT_FILEPATH}/introduction.md"
    OUTPUT_MAIN_TEXT: str = f"{OUTPUT_FILEPATH}/main_text.md"
    OUTPUT_CONCLUSION: str = f"{OUTPUT_FILEPATH}/conclusion.md"
    OUTPUT_CODE: str = f"{OUTPUT_FILEPATH}/code.md"
    OUTPUT_FINAL: str = f"{OUTPUT_FILEPATH}/final.md"

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
