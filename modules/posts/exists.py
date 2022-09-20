from modules import database
import hashlib

def exists_hash(data:bytes) -> bool:
    md5 = hashlib.md5(data).digest()
    sha256 = hashlib.sha256(data).digest()
    return any([
        database.Post.md5_exists(md5),
        database.Post.sha256_exists(sha256),
    ])
