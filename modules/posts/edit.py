import logging
from modules import database, schemas, validate
from typing import Union


def edit_post(
        post_id:int,
        editter_id:int,
        tags:Union[list[str], None] = None,
        source:Union[str, None] = None,
        rating:Union[str, None] = None,
        ):
    if tags == None and source == None and rating == None:
        raise PostEditFailure("Neither tags, nor source, nor rating was provided")

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
        raise PostEditFailure("Invalid Edit")

    try:
        database.Post.update(post_id,new_post)
    except Exception as e:
        logging.exception(e)
        raise PostEditFailure("Failed to Update Post")


class PostEditFailure(Exception):
    pass
