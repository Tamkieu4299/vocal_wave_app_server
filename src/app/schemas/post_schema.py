from typing import Optional, Union
from pydantic import UUID4, BaseModel
from datetime import datetime
import json
        
class PostResponseSchema(BaseModel):
    post_id: UUID4
    user_id: UUID4
    uploaded_link: Union[str, None]
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class CreatePostSchema(BaseModel):
    user_id: UUID4
    content: Union[str, None]
    uploaded_link: Union[str, None]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
