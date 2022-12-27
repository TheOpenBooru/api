from . import PostExistsException, exists_post
from modules.schemas.post import PostQuery
from modules import database, schemas

async def insert(post: schemas.Post, validate=True):
    """Insert post into the database
    Warning: Slow compared to direct insert
    
    Raises:
        - PostExistsException
    """
    if validate and exists_post(post):
        raise PostExistsException

    try:
        database.Post.insert(post)
    except:
        raise PostExistsException
    
    if post.uploader:
        database.User.create_post(post.uploader, post.id)


