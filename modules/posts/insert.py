from . import PostExistsException
from modules import database, schemas

def insert(post: schemas.Post, validate=True):
    """Insert post into the database, but check it exists
    Warning: Extremely slow compared to direct insert
    """
    if validate:
        _validate_post(post)

    database.Post.insert(post)
    if post.uploader:
        database.User.create_post(post.uploader, post.id)


def _validate_post(post: schemas.Post):
    for md5 in post.hashes.md5s:
        if database.Post.md5_exists(md5):
            raise PostExistsException
