from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import Message


class MessageRepository:
    async def get_messages(self, session: AsyncSession):
        query = select(Message).order_by(Message.created_at.asc())
        result = await session.execute(query)
        return result.fetchall()

    async def delete_message(self, session, message_id):
        query = select(Message).where(Message.id == message_id)
        result = await session.execute(query)
        message_to_delete = result.scalars().first()

        if message_to_delete:
            await session.delete(message_to_delete)
            await session.flush()
            return message_to_delete
        return message_to_delete

    async def update_message(self, session, message_id, content):
        query: Message = select(Message).where(Message.id == message_id)
        result = await session.execute(query)
        message_to_update = result.scalars().first()

        if message_to_update:
            message_to_update.content = content
            await session.flush()
            await session.refresh(message_to_update)
        return message_to_update

    async def add_messages(self, session: AsyncSession, user_id, content, user_name) -> Message:
        message = Message(
            user_id=user_id,
            content=content,
            user_name=user_name,
            created_at=datetime.now()
        )

        session.add(message)
        await session.flush()
        await session.refresh(message)
        return message
