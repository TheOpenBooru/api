from . import Importer, utils
from typing import Generator, Union
from modules import settings, schemas, database
from tqdm import tqdm
from time import strptime, mktime
import asyncio
from pathlib import Path
import ijson


class E621(Importer):
    enabled = settings.IMPORTER_E621_ENABLED
    def __init__(self):
        dump_path = Path(settings.IMPORTER_E621_DUMP)
        self.functional = dump_path.exists()


    async def load(self, limit:Union[int, None] = None):
        progress = tqdm(
            iterable=iter_over_posts(limit),
            total=limit or guess_post_count(),
            desc="Importing From E621 Dump",
            unit=" post",
        )

        for post in progress:
            await import_post(post)


def iter_over_posts(limit:Union[int, None]) -> Generator[dict, None, None]:
    post_count = 0
    with open(settings.IMPORTER_E621_DUMP) as f:
        parser = ijson.parse(f)
        for _, event, value in parser:
            if event == "start_map":
                yield parse_json_map(parser)
                post_count += 1
                if limit and post_count >= limit:
                    return


def parse_json_map(parser) -> dict:
    key = ""
    obj = {}
    for _, event, value in parser:
        if event == "map_key":
            key = value
        elif event == "start_map":
            obj[key] = parse_json_map(parser)
        elif event == "start_array":
            obj[key] = parse_json_array(parser)
        elif event == "boolean":
            obj[key] = value
        elif event == "string":
            obj[key] = value
        elif event == "number" :
            obj[key] = int(value)
        elif event == "end_map":
            return obj
    raise Exception("Invalid JSON")



def parse_json_array(parser) -> list:
    array = []
    for _, event, value in parser:
        if event == "start_map":
            array.append(parse_json_map(parser))
        elif event == "start_array":
            array.append(parse_json_array(parser))
        elif event == "boolean":
            array.append(value)
        elif event == "string":
            array.append(value)
        elif event == "number" :
            array.append(int(value))
        elif event == "end_array":
            return array
    raise Exception("Invalid JSON")


def guess_post_count() -> int:
    path = Path(settings.IMPORTER_E621_DUMP)
    stats = path.stat()
    size = stats.st_size
    AVG_POST_SIZE = 1682
    return size // AVG_POST_SIZE


async def import_post(data:dict):
    md5 = data['file']['md5']
    if database.Post.md5_exists(md5):
        return

    try:
        post = await post_from_dict(data)
        database.Post.insert(post)
    except Exception as e:
        pass


async def post_from_dict(post:dict) -> schemas.Post:
    full = construct_image(post['file'])
    preview = construct_image(post['sample'])
    thumbnail = construct_image(post['preview'])
    if full == None or thumbnail == None:
        raise Exception("Failed to Generate Images from E621 Post")

    return schemas.Post(
        id=database.Post.generate_id(),
        created_at=get_date(post['created_at']),
        media_type=utils.predict_media_type(post['file']['url']), # type: ignore
        full=full,
        preview=preview,
        thumbnail=thumbnail,
        tags=get_tags(post['tags']) + ["e621", full.type],
        source=get_source(post),
        upvotes=post['score']['up'],
        downvotes=post['score']['down'],
        hashes=schemas.Hashes(md5s=[post['file']['md5']]),
    )


def construct_image(image:dict) -> Union[schemas.Image, None]:
    if "url" in image:
        url = image["url"]
    elif 'ext' in image:
        ext = image['ext']
        md5 = image['md5']
        url = f"https://static1.e621.net/data/{md5[0:2]}/{md5[2:4]}/{md5}.{ext}"
    else:
        return None
    
    return schemas.Image(
        url=url,
        width=image["width"],
        height=image["height"],
        mimetype=utils.guess_mimetype(url),
        type=utils.predict_media_type(url), # type: ignore
    )


def get_source(post:dict) -> str:
    if post['sources']:
        return post['sources'][0]
    else:
        return f"https://e621.net/posts/{post['id']}"


def get_tags(tag_data:dict) -> list[str]:
    tags_set = set()
    tags_set.update(tag_data['general'])
    tags_set.update(tag_data['species'])
    tags_set.update(tag_data['character'])
    tags_set.update(tag_data['copyright'])
    tags_set.update(tag_data['artist'])
    tags_set.update(tag_data['lore'])
    tags_set.update(tag_data['meta'])
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
