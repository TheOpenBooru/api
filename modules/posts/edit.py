from . import PostEditFailure
from modules import database, schemas, validate
import logging
from typing import Union


def edit(
        post_id: int,
        editter_id: Union[int, None] = None,
        tags: Union[list[str], None] = None,
        sources: Union[list[str], None] = None,
        rating: Union[schemas.Rating, None] = None,
        ):
    if tags == None and sources == None and rating == None:
        raise PostEditFailure("No Changes Were Provided")

    for source in sources or []:
        if not validate.url(source):
            raise PostEditFailure("Source is not a valid URL")

    try:
        post = database.Post.get_id(post_id)
    except KeyError:
        raise PostEditFailure("Post does not exist")

    try:
        edit = schemas.PostEdit(
            post_id=post_id,
            editter_id=editter_id,
            sources=sources or post.sources,
            tags=tags or post.tags,
            rating=rating or post.rating,
        )
    except Exception as e:
        logging.exception(e)
        raise PostEditFailure("Attempted Edit was Invalid")

    try:
        database.Post.edit(post_id, edit)
    except Exception as e:
        logging.exception(e)
        raise PostEditFailure("Couldn't Update Post")


def apply_edit(
        post: schemas.Post,
        tags: Union[list[str], None] = None,
        sources: Union[list[str], None] = None,
        rating: Union[schemas.Rating, None] = None,
        ) -> schemas.Post:
    edit = schemas.PostEdit(
        post_id=post.id,
        editter_id=None,
        sources=sources or post.sources,
        tags=tags or post.tags,
        rating=rating or post.rating,
    )
    
    new_post = post.copy()
    new_post.sources = edit.sources
    new_post.tags = edit.tags
    new_post.rating = edit.rating
    new_post.edits.append(edit)
    return new_post
