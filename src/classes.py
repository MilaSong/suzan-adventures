from pydantic import BaseModel

class Answer(BaseModel):
    user_text: str