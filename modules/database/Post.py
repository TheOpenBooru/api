from modules import validate, schemas
from . import User
import time

_posts_store:dict[int,schemas.Post|None] = {}
class Post:
    @staticmethod
    def _verify_post(post:schemas.Post):
        # Valdiate hashes
        for md5 in post.md5s:
            assert validate.md5(md5)
            assert not bool(Post.get(md5=md5))
        for sha in post.sha256s:
            assert validate.sha256(sha)
            assert not bool(Post.get(sha256=sha))
        
        
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


    @staticmethod
    def get_unused_id() -> int:
        return len(_posts_store) + 1


    @staticmethod
    def create(post:schemas.Post):
        """Raises:
        - ValueError: If the post is invalid
        - KeyError: If the post is invalid
        """
        if post.id in _posts_store:
            raise KeyError("Post already exists")
        
        try:
            Post._verify_post(post)
        except AssertionError:
            raise ValueError("Invalid Post Data")
        
        _posts_store[post.id] = post


    @staticmethod
    def get(*,id:int|None=None,md5:str|None=None,sha256:str|None=None) -> schemas.Post | None:
        for post in _posts_store.values():
            if post == None:
                continue
            if ((id and post.id == id) or
                (md5 and md5 in post.md5s ) or
                (sha256 and sha256 in post.sha256s)):
                return post
        return None

    @staticmethod
    def update(id:int,new_version:schemas.Post):
        """Raises:
        - KeyError: Post not found
        """
        if id not in _posts_store:
            raise KeyError("Post not found")
        _posts_store[id] = new_version

    @staticmethod
    def search(limit:int=64,order:str='created_at',isAscending:bool=False,
            hasTags:list[str]=None,excludeTags:list[str]=None) -> list[schemas.Post]: # type: ignore
        """Raises:
        - ValueError: Invalid Ordering
        """
        hasTags = hasTags or []
        excludeTags = excludeTags or []
        
        def filterTags(post:schemas.Post) -> bool:
            if hasTags:
                for tag in hasTags:
                    return tag in post.tags
            if excludeTags:
                for tag in excludeTags:
                    return tag not in post.tags
            return True
        
        post_values = list(_posts_store.values())
        posts = [x for x in post_values if x != None] # type: ignore
        posts = filter(filterTags,posts)
        posts = list(posts)
        posts.sort(
            key=lambda post: getattr(post,order,0),
            reverse=not isAscending
        )
        return posts[:limit]


    @staticmethod
    def delete(id:int):
        try:
            _posts_store[id] = None
        except Exception:
            pass # Allow deleteion of non-existant posts


    @staticmethod
    def all() -> list[schemas.Post]:
        valid_posts = [x for x in _posts_store.values() if x != None]
        return valid_posts

    @staticmethod
    def clear():
        _posts_store.clear()


    @staticmethod
    def increment_view(id:int):
        if id in _posts_store and _posts_store[id] != None:
            _posts_store[id].views += 1 # type: ignore

