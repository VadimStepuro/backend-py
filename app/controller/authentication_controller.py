from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.login_request import LoginRequest
from app.dto.login_user import LoginUser
from app.dto.register_request import RegisterRequest
from app.dto.register_user import RegisterUser

from app.dependencies import get_user_repository, get_session

from app.repository.user_repository import UserRepository

from app.service.auth_service import verify_password, create_access_token


router = APIRouter()


@router.post("/login")
async def login(
        user_request: LoginRequest,
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    user_request: LoginUser = user_request.user

    user_db = await repository.get_user_by_username(session, user_request.username)

    if not user_db or not verify_password(user_request.password, user_db.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    data = {"username": user_db.username, "id": user_db.id}

    return {"user": data, "token": create_access_token(data)}


@router.post("/register")
async def register(
        user: RegisterRequest,
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    user: RegisterUser = user.user

    if user.password != user.confirmation_password:
        raise HTTPException(status_code=400, detail="Password is not equal")

    users_db = await repository.get_user_by_username(session, user.username)

    if users_db:
        print(users_db)
        raise HTTPException(status_code=400, detail="Username already registered")

    user = await repository.create_user(session, user.username, user.password)

    return {"username": user.username, "message": "User successfully registered"}