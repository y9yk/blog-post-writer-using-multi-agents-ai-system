import os
from functools import lru_cache
from os import path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    기본 Configuration
    """

    PROJECT_ROOT: str = path.dirname(
        path.dirname(
            path.dirname(
                path.dirname(
                    (path.abspath(__file__)),
                ),
            ),
        )
    )

    PROJECT_NAME: str = "blog_poster-backend"
    PROJECT_DESC: str = ""

    DEBUG: bool = True

    # project
    API_PREFIX: str = f"/blog_poster/api"
    API_HC_PREFIX: str = f"/blog_poster"

    AUTH_ALGORITHM: str = "HS256"

    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASS: str = "password"
    DB_NAME: str = "blog_poster"
    DB_PORT: str = "3306"
    DB_POOL_PRE_PING: bool = True
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = False

    class Config:
        env_prefix = ""
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
