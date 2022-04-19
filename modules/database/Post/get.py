from . import _posts_store,Post

def get(*,id:int|None=None,md5:str|None=None,sha256:str|None=None) -> Post | None:
    for post in _posts_store.values():
        if post.deleted:
            continue
        if ((id and post.id == id) or 
            (md5 and md5 in post.md5s) or
            (sha256 and sha256 in post.sha256s)):
            return post
    return None