from sqlalchemy.orm import (
    Session,
)
from sqlalchemy import desc, asc
from ..models.post_model import Post

def create_post(post: Post, db: Session) -> Post:
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def read_post(post_id: str, db: Session) -> Post:
    post = (
        db.query(Post).filter(Post.post_id == post_id).first()
    )
    return post

async def all_posts(db: Session) -> list[Post]:
    db_posts = db.query(Post).order_by(desc(Post.created_at)).all()
    return db_posts

def search_posts_by_user_id(user_id: str, db: Session):
    db_items = db.query(Post).filter(Post.user_id == user_id).order_by(desc(Post.created_at)).all()
    return db_items
