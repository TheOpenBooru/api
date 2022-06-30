from . import Post, post_collection
from modules import validate,database
import time

def is_post_unique(post:Post) -> bool:
    MD5_Filter = {'md5s':{"$in":post.hashes.md5s}}
    SHA_Filter = {'sha256s':{"$in":post.hashes.sha256s}}
    
    if database.Post.exists(post.id):
        return False
    elif post.hashes.md5s and post_collection.find_one(MD5_Filter):
        return False
    elif post.hashes.sha256s and post_collection.find_one(SHA_Filter):
        return False
    else:
        return True


def is_post_valid(post:Post) -> bool:
    try:
        # Generic types
        assert post.created_at < time.time()
        assert validate.post_type(post.media_type)
        
        #! Disabled because Users aren't implemented
        # assert User.exists(post.uploader)
        
        # Valdiate hashes
        for md5 in post.hashes.md5s:
            assert validate.md5(md5)
        for sha in post.hashes.sha256s:
            assert validate.sha256(sha)
        
        for tag in post.tags:
            validate.tag(tag)
        
        # Validate Image URLs
        if post.full: assert validate.url(post.full.url)
        if post.thumbnail: assert validate.url(post.thumbnail.url)
        if post.preview: assert validate.url(post.preview.url)
    except AssertionError:
        return False
    else:
        return True
