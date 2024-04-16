
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .events import create_start_app_handler, create_stop_app_handler
from app.controller.websockets_controller import router as websockets_router


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

    application.include_router(websockets_router.router, tags=["websockets"], prefix="/ws")

    return application


app = get_application()


if __name__ == "__mian__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
