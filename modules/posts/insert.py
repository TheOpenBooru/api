from modules.schemas.post import PostQuery
from . import PostExistsException
from modules import database, schemas

async def insert(post: schemas.Post, validate=True):
    """Insert post into the database, but check it exists
    Warning: Extremely slow compared to direct insert
    """
    if validate:
        await _validate_post(post)

    database.Post.insert(post)
    if post.uploader:
        database.User.create_post(post.uploader, post.id)


async def _validate_post(post: schemas.Post):
    for md5 in post.hashes.md5s:
        if database.Post.md5_exists(md5):
            raise PostExistsException

    for sha256 in post.hashes.sha256s:
        if database.Post.sha256_exists(sha256):
            raise PostExistsException
    
    for phash in post.hashes.phashes:
        if database.Post.phash_exists(phash):
            raise PostExistsException
