from .. import utils, ImportFailure
from modules import schemas
from typing import Union
from time import strptime, mktime

def construct_image(image:dict) -> Union[schemas.Image, None]:
    if "url" in image:
        url = image["url"]
    elif 'ext' in image:
        ext = image['ext']
        md5 = image['md5']
        url = f"https://static1.e621.net/data/{md5[0:2]}/{md5[2:4]}/{md5}.{ext}"
    else:
        return None
    try:
        media_type = utils.predict_media_type(url)
    except Exception:
        raise ImportFailure("Unsupported File Type")
    
    return schemas.Image(
        url=url,
        width=image["width"],
        height=image["height"],
        mimetype=utils.guess_mimetype(url),
        type=media_type, # type: ignore
    )


def get_source(post:dict) -> str:
    if post['sources']:
        return post['sources'][0]
    else:
        return f"https://e621.net/posts/{post['id']}"


def get_tags(data:dict, type:str) -> list[str]:
    tag_data = data['tags']
    tags_set = set()
    tags_set.update(tag_data['general'])
    tags_set.update(tag_data['species'])
    tags_set.update(tag_data['character'])
    tags_set.update(tag_data['copyright'])
    tags_set.update(tag_data['artist'])
    tags_set.update(tag_data['lore'])
    tags_set.update(tag_data['meta'])
    tags_set.add(type)
    tags_set.add("e621")
    tags = utils.normalise_tags(list(tags_set))
    return tags


def get_date(dateString:str) -> int:
    FORMAT_1 = r"%Y-%m-%dT%H:%M:%S.%f%z"
    FORMAT_2 = r"%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        time_struct = strptime(dateString,FORMAT_1)
    except Exception:
        time_struct = strptime(dateString,FORMAT_2)
    timestamp = int(mktime(time_struct))
    return timestamp


def get_upvotes(data) -> int:
    return data['score']['up']


def get_downvotes(data) -> int:
    return data['score']['down'] * -1
