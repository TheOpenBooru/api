from . import Post, _posts_store
from modules import schemas

def search(query:schemas.Post_Query) -> list[Post]:
    """Raises:
    - ValueError: Invalid Ordering
    """
    def filterTags(post:Post) -> bool:
        valid = True
        if query.include_tags:
            for tag in query.include_tags:
                valid = valid and tag in post.tags
        if query.exclude_tags:
            for tag in query.exclude_tags:
                valid = valid and tag not in post.tags
        return valid
    
    post_values = list(_posts_store.values())
    posts = [x for x in post_values if x != None] # type: ignore
    posts = filter(filterTags,posts)
    posts = list(posts)
    posts.sort(
        key=lambda post: getattr(post,query.sort,0),
        reverse=not query.descending
    )
    return posts[query.index:query.limit + query.index]
