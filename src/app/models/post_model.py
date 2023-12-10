import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# inquiry Model
class Post(Base):
    __tablename__ = "posts"
    post_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    uploaded_link = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    class Config:
        orm_mode = True
