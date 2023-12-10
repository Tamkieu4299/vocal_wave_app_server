import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..crud.post_crud import (
    all_posts,
    create_post,
    read_post,
    search_posts_by_user_id,
)
from ..crud.user_crud import update_user_performance, read_user


from ..db.database import get_db
from ..models.post_model import Post
from ..schemas.post_schema import (
    CreatePostSchema,
    PostResponseSchema,
)
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
)
async def add_post(
    post_data: CreatePostSchema,
    db: Session = Depends(get_db),
):

    post: Post = Post(**post_data.dict())
    new_post = create_post(post, db)
    
    logger.info(
        f"Created post with ID {new_post.post_id}"
    )

    return new_post.__dict__

@router.get("/get/{post_id}", response_model=PostResponseSchema)
async def get_post_by_id(post_id: str, db: Session = Depends(get_db)):
    """Get the post by its id"""
    post = read_post(post_id, db)
    if post is None:
        logger.info(f"Invalid post with ID: {post_id}")
        raise NotFoundException(
            detail=f"Invalid post with ID: {post_id}"
        )

    logger.info(f"Get post with ID: {post.post_id}")
    return post.__dict__


@router.get("/search/", response_model=List[PostResponseSchema])
async def get_posts(db: Session = Depends(get_db)):
    posts = all_posts(db)
    
    posts_dict_list = []
    for post in posts:
        post_dict = post.__dict__
        posts_dict_list.append(post_dict)

    logger.info(f"Number of posts: {len(posts)}")
    return posts_dict_list


@router.get("/search-by-user-id/{user_id}", response_model=List[PostResponseSchema])
async def search_by_user_id(user_id: str, db: Session = Depends(get_db)):
    posts = search_posts_by_user_id(user_id, db)
    posts_dict_list = []
    for post in posts:
        post_dict = post.__dict__
        posts_dict_list.append(post_dict)
    logger.info(f"Number of posts: {len(posts)}")
    return posts_dict_list
