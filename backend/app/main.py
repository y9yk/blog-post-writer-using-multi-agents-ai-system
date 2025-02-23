from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from backend.app.clients import websocket_manager
from backend.app.databases.mysql import mysql_session_manager
from backend.app.errors import (
    APIException,
    api_exception_handler,
    global_exception_handler,
    validation_exception_handler,
)
from backend.app.middlewares import HttpRequestLoggingMiddleware
from backend.app.modules.api import api_router, hc_api_router
from backend.app.utils import get_root_logger
from config import settings


# lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize databases
    mysql_session_manager.init_app()

    # initialize websocket manager
    websocket_manager.init_app()

    # create tables
    await mysql_session_manager.create_tables()

    yield

    # shutdown gracefully
    if mysql_session_manager._engine is not None:
        await mysql_session_manager.close()

    await websocket_manager.close()


# create application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESC,
    docs_url="/blog_poster/doc",
    openapi_url="/blog_poster/openapi.json",
    lifespan=lifespan,
)

# register middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HttpRequestLoggingMiddleware, logger=get_root_logger())

# register exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# register router (HealthChecking)
app.include_router(
    hc_api_router,
    prefix=settings.API_HC_PREFIX,
)

# register router (APIs)
app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
    # dependencies=(
    #     [
    #         Depends(
    #             verify,
    #         )
    #     ]
    # ),
)

# include websocket_manager to app
app.state.websocket_manager = websocket_manager
