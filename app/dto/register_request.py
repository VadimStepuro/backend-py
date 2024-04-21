from pydantic import BaseModel
from app.dto.register_user import RegisterUser


class RegisterRequest(BaseModel):
    user: RegisterUser
