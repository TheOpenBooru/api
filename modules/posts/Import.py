from . import PostExistsException, PostImportFailure
from modules import importers, database, posts
from typing import Union

async def Import(url:str, user_id: Union[int, None] = None):
    if database.Post.exists(sources=[url]):
        return PostImportFailure("Post Already Exists")
    
    try:
        new_posts = await importers.download_url(url)
    except importers.DownloadFailure as e:
        return PostImportFailure(e.message)
    except Exception:
        return PostImportFailure("Unknown Error")

    for post in new_posts:
        post.uploader = user_id
        await posts.insert(post)
    
    return new_posts