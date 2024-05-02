from app.model.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.service.auth_service import hash_password


class UserRepository:
    async def get_user(self, session: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)

        result = await session.execute(query)

        user = result.scalars().first()

        return user

    async def get_user_by_username(self, session: AsyncSession, username: str):
        query = select(User).where(User.username == username)

        result = await session.execute(query)

        user = result.scalars().first()

        return user

    async def create_user(self, session: AsyncSession, username, password):
        hashed_password = hash_password(password)

        user = User(username=username, password=hashed_password)

        session.add(user)

        await session.flush()
        await session.refresh(user)

        return user
