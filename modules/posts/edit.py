from . import PostEditFailure
from modules import database, schemas, validate
import logging
from typing import Union


def edit_post(
        post_id:int,
        editter_id:Union[int, None],
        tags:Union[list[str], None] = None,
        source:Union[str, None] = None,
        rating:Union[schemas.Rating, None] = None,
        ):
    if tags == None and source == None and rating == None:
        raise PostEditFailure("No Changes Were Provided")

    if source and not validate.url(source):
        raise PostEditFailure("Source is not a valid URL")
    
    try:
        old_post = database.Post.get(post_id)
    except KeyError:
        raise PostEditFailure("Post does not exist")

    new_post = old_post.copy()
    if tags != None:
        new_post.tags = tags
    if source != None:
        new_post.source = source
    if rating != None:
        new_post.rating = rating
    
    try:
        edit = schemas.Post_Edit(
            post_id=post_id,
            editter_id=editter_id,
            old_source=old_post.source,
            new_source=new_post.source,
            old_tags=old_post.tags,
            new_tags=new_post.tags,
            old_rating=old_post.rating,
            new_rating=new_post.rating,
        )
        new_post.edits.append(edit)
    except Exception as e:
        logging.exception(e)
        raise PostEditFailure("Attempted Edit was Invalid")

    try:
        database.Post.update(post_id,new_post)
    except Exception as e:
        logging.exception(e)
        raise PostEditFailure("Couldn't Update Post")


