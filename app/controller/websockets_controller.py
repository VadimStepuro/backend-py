
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.message_repository import MessageRepository
from app.configs.connection_manager import ConnectionManger
from app.dependencies import get_session, get_message_repository_ws, get_manager_ws


router = APIRouter()


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
    repository: MessageRepository = Depends(get_message_repository_ws),
    manager: ConnectionManger = Depends(get_manager_ws)
):
    try:
        await websocket.accept()

        manager.add(websocket)

        chat_history = await repository.get_messages(session)

        await websocket.send_json({
            "message": {
                "type": "connection",
                "data": [i._asdict()['Message'].to_json_object() for i in chat_history]
            }
        })

        print("New connection was established with " + str(websocket.headers))

        while True:
            await websocket.receive_json()
    except Exception as e:
        print("Error in websocket:", e)

        await manager.remove(websocket)

        return HTTPException(status_code=500, detail="Error in websocket")
