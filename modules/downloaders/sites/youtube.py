import mimetypes
from typing import Union
from . import utils, Downloader, DownloadFailure
from modules import settings, schemas, posts
import pytube


class Youtube(Downloader):
    enabled = settings.DOWNLOADER_YOUTUBE_ENABLED
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
            
            data, _ = utils.download_url(stream.url) # type: ignore
            filename = "example" + mimetypes.guess_extension(stream.mime_type) # type: ignore
        except Exception:
            raise DownloadFailure("Could not download Video")

        try:
            post = await posts.generate(data, filename,
                additional_tags=await getTags(video),
                source=video.watch_url,
            )
        except Exception:
            raise DownloadFailure("Could not generate post from video")
        
        
        return [post]



async def getTags(video: pytube.YouTube) -> list[str]:
    tags = set()
    keywords = video.vid_info['videoDetails']['keywords']
    keywords = utils.normalise_tags(keywords)
    tags.update(keywords)
    
    author = await getAuthorName(video)
    if author:
        tags.add(author)
    
    return list(tags)


async def getAuthorName(video:pytube.YouTube) -> Union[str,None]:
    channel = pytube.Channel(video.channel_url)
    try:
        name = channel.initial_data['header']['c4TabbedHeaderRenderer']['title'] #type: ignore
    except Exception:
        return None
    else:
        author = utils.normalise_tag(name,possibly_namespaced=False)
        return author
