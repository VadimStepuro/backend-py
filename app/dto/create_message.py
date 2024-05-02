from pydantic import BaseModel


class CreateMessage(BaseModel):
    user_id: int
    content: str
