from typing import Optional, Union
from pydantic import UUID4, BaseModel
from datetime import datetime
        
class PostResponseSchema(BaseModel):
    post_id: UUID4
    user_id: UUID4
    uploaded_link: str
    content: str

    class Config:
        orm_mode = True

class CreatePostSchema(BaseModel):
    user_id: UUID4
    uploaded_link: Union[str, None]
    content: Union[str, None]

    class Config:
        orm_mode = True
