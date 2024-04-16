from typing import Callable
from fastapi import FastAPI

from app.configs.connection_manager import ConnectionManger
from app.repository.message_repository import MessageRepo
from app.repository.user_repository import UserRepository


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        app.state.repositories = {
            "userRepo": UserRepository(),
            "messageRepo": MessageRepo(),
        }
        app.state.manager = ConnectionManger()
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        pass

    return stop_app