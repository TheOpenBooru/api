from . import PostExistsException, PostImportFailure
from modules import downloaders, database, posts
from typing import Union

async def Import(url:str, user_id: Union[int, None] = None):
    if database.Post.source_exists(url):
        return PostImportFailure("Post Already Exists")
    
    try:
        new_posts = await downloaders.download_url(url)
    except downloaders.DownloadFailure as e:
        return PostImportFailure(e.message)
    except Exception:
        return PostImportFailure("Unknown Error")

    for post in new_posts:
        post.uploader = user_id
        await posts.insert(post)
    
    return new_posts