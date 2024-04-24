
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from events import create_start_app_handler, create_stop_app_handler
from app.controller.websockets_controller import router as websockets_router
from app.controller.authentication_controller import router as authentication_router
from app.controller.message_controller import router as message_controller

from dotenv import load_dotenv


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins='http://localhost:8080',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application),
    )

    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    application.include_router(websockets_router, tags=["websockets"], prefix="/cable")
    application.include_router(authentication_router, tags=["authentication"], prefix="")
    application.include_router(message_controller, tags=["messages"], prefix="/messages")

    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
