from . import Post, post_collection
from modules import database

def is_post_unique(post:Post) -> bool:
    MD5_Filter = {'hashes.md5s':{"$in":post.hashes.md5s}}
    SHA_Filter = {'hashes.sha256s':{"$in":post.hashes.sha256s}}
    
    if database.Post.exists(post.id):
        return False
    elif post.hashes.md5s and post_collection.find_one(MD5_Filter):
        return False
    elif post.hashes.sha256s and post_collection.find_one(SHA_Filter):
        return False
    else:
        return True
