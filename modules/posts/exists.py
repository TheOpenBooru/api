from modules import database, schemas
from modules.database.Post import exists
import hashlib

def exists_data(data:bytes) -> bool:
    md5 = hashlib.md5(data).digest()
    sha256 = hashlib.sha256(data).digest()
    return database.Post.exists(
        md5s=[md5],
        sha256s=[sha256],
    )


def exists_hashes(hashes:schemas.Hashes) -> bool:
    return database.Post.exists(
        md5s=hashes.md5s,
        sha256s=hashes.sha256s,
        phashes=hashes.phashes,
    )


def exists_post(post: schemas.Post):
    return exists(
        id=post.id,
        sources=post.sources,
        md5s=post.hashes.md5s,
        sha256s=post.hashes.sha256s,
        phashes=post.hashes.phashes,
    )
