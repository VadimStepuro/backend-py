from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.connection_manager import ConnectionManger
from app.dependencies import get_message_repository, get_session, get_manager, get_user_repository
from app.dto.create_message_request import CreateMessageRequest
from app.dto.edit_message_request import EditMessageRequest
from app.repository.message_repository import MessageRepository
from app.repository.user_repository import UserRepository

router = APIRouter()


@router.post("")
async def create_message(
        create_message_request: CreateMessageRequest,
        session: AsyncSession = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository),
        message_repository: MessageRepository = Depends(get_message_repository),
        manager: ConnectionManger = Depends(get_manager)
):
    user = await user_repository.get_user(session, create_message_request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    created_message = await message_repository.add_message(
        session,
        create_message_request=create_message_request,
        user_name=user.username
    )

    print("Message " + str(created_message) + " created")

    await manager.broadcast("create", created_message.to_json_object())

    return created_message.to_json_object()


@router.patch("/{message_id}")
async def edit_message(
        message_id: int,
        edit_message_request: EditMessageRequest,
        session: AsyncSession = Depends(get_session),
        repository: MessageRepository = Depends(get_message_repository),
        manager: ConnectionManger = Depends(get_manager)
):
    edited_message = await repository.update_message(session, message_id, edit_message_request.content)

    print("Message " + str(edited_message) + " edited")

    all_messages = await repository.get_messages(session)
    all_messages = [i._asdict()['Message'].to_json_object() for i in all_messages]

    await manager.broadcast("update", all_messages)

    return edit_message_request.to_json_object()


@router.delete("/{message_id}")
async def delete_message(
        message_id: int,
        session: AsyncSession = Depends(get_session),
        repository: MessageRepository = Depends(get_message_repository),
        manager: ConnectionManger = Depends(get_manager)
):
    await repository.delete_message(session, message_id)

    print("Message with id " + str(message_id) + " deleted")

    all_messages = await repository.get_messages(session)
    all_messages = [i._asdict()['Message'].to_json_object() for i in all_messages]

    await manager.broadcast("destroy", all_messages)

    return {}
