from fastapi import Request, WebSocket

from app.configs.db_config import AsyncSessionLocal


async def get_user_repository(request: Request):
    return request.app.state.repositories["userRepo"]


async def get_message_repository(request: Request):
    return request.app.state.repositories["messageRepo"]


async def get_user_repository_ws(request: WebSocket):
    return request.app.state.repositories["userRepo"]


async def get_message_repository_ws(request: WebSocket):
    return request.app.state.repositories["messageRepo"]


async def get_manager(request: Request):
    return request.app.state.manager


async def get_manager_ws(request: WebSocket):
    return request.app.state.manager


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()

        except:
            await session.rollback()

        finally:
            await session.close()
