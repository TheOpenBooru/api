from openbooru.modules import schemas, normalise
from openbooru.modules.schemas import Media, Image, MediaType, Rating
from openbooru.modules.importers import utils, DownloadFailure
from typing import Union, Callable
from time import strptime, mktime
import e621.models as e621Models


def construct_image(media: dict) -> Union[Media, None]:
    if "url" in media:
        url = media["url"]
    elif 'ext' in media:
        ext = media['ext']
        md5 = media['md5']
        url = f"https://static1.e621.net/data/{md5[0:2]}/{md5[2:4]}/{md5}.{ext}"
    else:
        return None
    
    try:
        media_type = utils.predict_media_type(url)
    except Exception:
        raise DownloadFailure("Unsupported File Type")

    if media_type == MediaType.image:
        media_class = schemas.Image
    elif media_type == MediaType.image:
        media_class = schemas.Animation
    else:
        media_class = schemas.Video
    
    return media_class(
        url=url,
        width=media["width"],
        height=media["height"],
        mimetype=utils.guess_mimetype(url),
        type=media_type,
    )


def get_images(post: dict) -> tuple[Media, Media|None, Image]:
    full = construct_image(post['file'])
    preview = construct_image(post['sample'])
    thumbnail = construct_image(post['preview'])

    if not isinstance(full, Media):
        raise DownloadFailure("Failed to Generate Images from E621 Post")
    
    if not isinstance(thumbnail,Image):
        raise DownloadFailure("Failed to Generate Images from E621 Post")
    
    return full, preview, thumbnail


def get_sources(hostname: str) -> Callable[[dict],list[str]]:
    def inner(post: dict) -> list[str]:
        sources = [f"https://{hostname}/posts/{post['id']}"]
        sources.extend(post['sources'])
        return sources
    
    return inner


def get_hashes(data: dict) -> schemas.Hashes:
    md5 = data["file"]["md5"]
    return schemas.Hashes(md5s=[md5])

def get_tags(data: dict) -> list[str]:
    tags = []
    tag_data = data['tags']
    tags.extend(tag_data['general'])
    tags.extend(tag_data['species'])
    tags.extend(tag_data['character'])
    tags.extend(tag_data['copyright'])
    tags.extend(tag_data['artist'])
    tags.extend(tag_data['lore'])
    tags.extend(tag_data['meta'])
    tags.extend(tag_data['meta'])
    tags.append("e621")
    tags = normalise.normalise_tags(tags)
    return tags


def get_date(data: dict) -> int:
    FORMAT_1 = r"%Y-%m-%dT%H:%M:%S.%f%z"
    FORMAT_2 = r"%Y-%m-%dT%H:%M:%S.%fZ"
    date_string = data["created_at"]
    try:
        time_struct = strptime(date_string,FORMAT_1)
    except Exception:
        time_struct = strptime(date_string,FORMAT_2)
    timestamp = int(mktime(time_struct))
    return timestamp


def get_rating(data: dict) -> Rating:
    rating = data["rating"]
    if rating == "e":
        return Rating.explicit
    elif rating == "q":
        return Rating.mature
    elif rating == "s":
        return Rating.safe
    else:
        return Rating.unrated

def get_upvotes(data: dict) -> int:
    return data['score']['up']


def get_downvotes(data: dict) -> int:
    return data['score']['down'] * -1
