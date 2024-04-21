from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.configs.connection_manager import ConnectionManger

from app.repository.message_repository import MessageRepository
from app.repository.user_repository import UserRepository

from app.dto.create_message import CreateMessage
from app.dto.edit_message import EditMessage

from app.dependencies import get_message_repository, get_session, get_manager, get_user_repository


router = APIRouter()


@router.post("")
async def messages(
        message: CreateMessage,
        session: AsyncSession = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository),
        message_repository: MessageRepository = Depends(get_message_repository),
        manager: ConnectionManger = Depends(get_manager)
):
    user = await user_repository.get_user(session, message.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    message = await message_repository.add_messages(
        session,
        user_id=message.user_id,
        content=message.content,
        user_name=user.username
    )

    await manager.broadcast("create", message.to_dict())

    return message.to_dict()


@router.patch("/{message_id}")
async def messages(
        message_id: int,
        data: EditMessage,
        session: AsyncSession = Depends(get_session),
        repository: MessageRepository = Depends(get_message_repository),
        manager: ConnectionManger = Depends(get_manager)
):
    await repository.update_message(session, message_id, data.content)

    all_messages = await repository.get_messages(session)

    all_messages = [i._asdict()['Message'].to_dict() for i in all_messages]

    await manager.broadcast("update", all_messages)

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/{message_id}")
async def messages(
        message_id: int,
        session: AsyncSession = Depends(get_session),
        repository: MessageRepository = Depends(get_message_repository),
        manager: ConnectionManger = Depends(get_manager)
):
    await repository.delete_message(session, message_id)

    all_messages = await repository.get_messages(session)

    all_messages = [i._asdict()['Message'].to_dict() for i in all_messages]

    await manager.broadcast("destroy", all_messages)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
