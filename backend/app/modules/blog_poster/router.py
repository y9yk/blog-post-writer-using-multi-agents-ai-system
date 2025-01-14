import json

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from backend.app.clients import WebSocketManager
from backend.app.modules.blog_poster import BlogPosterRequest, BlogPosterService

router = APIRouter(
    tags=["BLOG_POSTER"],
)


@router.websocket("/ws")
async def websocket_endpoint(request: Request, websocket: WebSocket):
    #
    blog_poster_service = BlogPosterService()

    #
    websocket_manager: WebSocketManager = request.app.state.websocket_manager
    await websocket_manager.connect(websocket=websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)

            # validate and setting request obj.
            BlogPosterRequest.model_validate(data)
            blog_poster_request = BlogPosterRequest(**json.loads(data))

            # call service
            blog_poster_service.process(
                **blog_poster_request.model_dump(),
                websocket=websocket,
            )

    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket=websocket)
