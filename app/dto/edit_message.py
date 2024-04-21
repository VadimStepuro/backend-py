from pydantic import BaseModel


class EditMessage(BaseModel):
    user_id: int
    content: str
