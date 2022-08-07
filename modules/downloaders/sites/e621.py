from typing import Union
from . import URLImporter, utils, ImportFailure
from modules import settings, schemas, posts
from e621.api import E621 as _E621
import e621.models as e621Models
import re


class E621(URLImporter):
    enabled = settings.E621_ENABLED
    api:_E621
    def __init__(self):
        try:
            self.api = _E621()
            self.api.posts.search()
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self,url:str) -> bool:
        return url.startswith("https://e621.net/posts/")


    async def download_url(self,url:str) -> list[schemas.Post]:
        id = id_from_url(url)
        try:
            e621_post = self.api.posts.get(id)
        except Exception:
            raise ImportFailure("Could not find E621 Post")

        data, filename = utils.download_url(e621_post.file.url) # type: ignore
        source = source_from_post(e621_post)
        tags = combine_tags(e621_post)
        post = await posts.generate(data, filename,
            source=source,
            additional_tags=tags,
        )
        return [post]


def id_from_url(url:str) -> int:
    id_match = re.match(r"^https:\/\/e621.net\/posts\/[0-9]*$", url)
    if id_match == None:
        raise ImportFailure("Could not find e621 ID in URL")
    id = id_match.group().split("/")[-1]
    id = int(id)
    return id


def source_from_post(post: e621Models.Post) -> str:
    if post.sources:
        return post.sources[0]
    else:
        return f"https://e621.net/posts/{post.id}"


def combine_tags(post: e621Models.Post) -> list[str]:
    tags = []
    tags.extend(post.tags.artist)
    tags.extend(post.tags.character)
    tags.extend(post.tags.copyright)
    tags.extend(post.tags.general)
    tags.extend(post.tags.meta)
    tags.extend(post.tags.species)
    tags = utils.normalise_tags(tags)
    return tags