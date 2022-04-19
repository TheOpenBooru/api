from . import get,Post

def is_post_unique(post:Post) -> bool:
    if get.get(id=post.id):
        return False
    for md5 in post.md5s:
        if get.get(md5=md5) != None:
            return False
    for sha in post.sha256s:
        if get.get(sha256=sha) != None:
            return False
    return True


def is_post_valid(post:Post) -> bool:
    return True
    # Valdiate hashes
    for md5 in post.md5s:
        assert validate.md5(md5)
    for sha in post.sha256s:
        assert validate.sha256(sha)
    
    
    # Validate Image URLs
    assert validate.url(post.full.url)
    assert validate.url(post.thumbnail.url)
    if post.preview:
        assert validate.url(post.preview.url)
    
    for tag in post.tags:
        validate.tag(tag)
    validate.language(post.language) if post.language else None
    validate.rating(post.age_rating) if post.age_rating else None
    
    assert post.created_at < time.time(), "Created in the future"
    assert validate.post_type(post.type), f"Invalid post type: {post.type}"

    # !User's are not implemented
    # if not User.exists(post.uploader):
    #     raise ValueError("Invalid User ID")
