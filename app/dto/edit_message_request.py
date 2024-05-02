from pydantic import BaseModel


class EditMessageRequest(BaseModel):
    user_id: int
    content: str

    def to_json_object(self):
        return {
            'user_id': self.user_id,
            'content': self.content
        }