from pydantic import BaseModel
from app.dto.login_user import LoginUser


class LoginRequest(BaseModel):
    user: LoginUser
