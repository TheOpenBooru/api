from modules import normalise
from modules.importers import Downloader, DownloadFailure, utils
import mimetypes
from typing import Union
from modules import settings, schemas, posts
import pytube


class YoutubeDownloader(Downloader):
    def __init__(self):
        # Test Connection to Youtube
        pytube.YouTube("https://youtu.be/GLlLQ3LmZWU")


    def is_valid_url(self,url:str) -> bool:
        return any((
            url.startswith("https://www.youtube.com/watch?v="),
            url.startswith("https://youtube.com/watch?v="),
            url.startswith("https://youtu.be/"),
        ))

    async def download_url(self,url:str) -> list[schemas.Post]:
        video = pytube.YouTube(url)

        try:
            stream = video.streams.get_by_resolution("720p")
            if stream == None:
                stream = video.streams.get_highest_resolution()
            
            data, _ = await utils.download_url(stream.url) # type: ignore
            filename = "example" + mimetypes.guess_extension(stream.mime_type) # type: ignore
        except Exception:
            raise DownloadFailure("Could not download Video")

        try:
            post = await posts.generate(data, filename)
            tags = get_tags(video)
        except Exception:
            raise DownloadFailure("Could not generate post from video")
        
        post = posts.apply_edit(
            post=post,
            tags=tags,
            sources=[video.watch_url],
        )
        return [post]



def get_tags(video: pytube.YouTube) -> list[str]:
    tags = set()
    keywords = video.vid_info['videoDetails']['keywords']
    keywords = normalise.normalise_tags(keywords)
    tags.update(keywords)
    
    author = get_author_name(video)
    if author:
        tags.add(author)
    
    return list(tags)


def get_author_name(video:pytube.YouTube) -> Union[str,None]:
    channel = pytube.Channel(video.channel_url)
    try:
        name = channel.initial_data['header']['c4TabbedHeaderRenderer']['title'] #type: ignore
    except Exception:
        return None
    else:
        author = normalise.normalise_tag(name)
        return author
