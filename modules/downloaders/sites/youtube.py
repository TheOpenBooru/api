import mimetypes
from typing import Union
from . import utils, URLImporter, ImportFailure
from modules import settings, schemas, posts
import pytube


class Youtube(URLImporter):
    enabled = settings.YOUTUBE_ENABLED
    def __init__(self):
        try:
            pytube.YouTube("https://youtu.be/GLlLQ3LmZWU")
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self,url:str) -> bool:
        return any((
            url.startswith("https://www.youtube.com/watch?v="),
            url.startswith("https://youtube.com/watch?v="),
            url.startswith("https://youtu.be/"),
        ))

    async def download_url(self,url:str) -> list[schemas.Post]:
        video = pytube.YouTube(url)


        try:
            stream = video.streams.get_highest_resolution()
            data, _ = utils.download_url(stream.url)
            filename = "example" + mimetypes.guess_extension(stream.mime_type)
        except Exception:
            raise ImportFailure("Could not download Video")

        try:
            post = await posts.generate(data, filename)
        except Exception:
            raise ImportFailure("Could not generate post from video")
        
        post.source = video.watch_url

        author = getAuthorName(video)
        if author:
            post.tags.append(author)
        
        return [post]


def getAuthorName(video:pytube.YouTube) -> Union[str,None]:
    channel = pytube.Channel(video.channel_url)
    try:
        name = channel.initial_data['header']['c4TabbedHeaderRenderer']['title'] #type: ignore
    except Exception:
        return None
    else:
        author = utils.normalise_tag(name,possibly_namespaced=False)
        return author