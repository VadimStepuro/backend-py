from fastapi import Request, WebSocket

from app.configs.db_config import AsyncSessionLocal

async def get_userRepository(request: Request):
    return request.app.state.repositories["userRepo"]
async def get_messageRepository(request: Request):
    return request.app.state.repositories["messageRepo"]
async def get_userRepository_ws(request: WebSocket):
    return request.app.state.repositories["userRepo"]
async def get_messageRepository_ws(request: WebSocket):
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