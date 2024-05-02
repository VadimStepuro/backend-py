from pydantic import BaseModel


class CreateMessageRequest(BaseModel):
    user_id: int
    content: str
