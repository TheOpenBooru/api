from . import Importer, utils
from typing import Generator, Union
from modules import settings, schemas, database
from modules.importers.classes import ImportFailure
from tqdm import tqdm
from time import strptime, mktime
from pathlib import Path
import ijson


class E621(Importer):
    enabled = settings.IMPORTER_E621_ENABLED
    time_between_runs = settings.IMPORTER_E621_RETRY_AFTER
    def __init__(self):
        dump_path = Path(settings.IMPORTER_E621_DUMP)
        if dump_path.exists() == False:
            raise FileNotFoundError("Could not find e621 dump")


    async def load(self, limit:Union[int, None] = None):
        progress = tqdm(
            iterable=iter_over_posts(limit),
            total=limit or guess_post_count(),
            desc="Importing From E621 Dump",
            unit=" post",
        )

        for data in progress:
            try:
                await load_post(data)
            except ImportFailure:
                pass


async def load_post(data:dict):
    try:
        md5 = data['file']['md5']
        post = database.Post.getByMD5(md5)
    except KeyError:
        await import_post(data)
    else:
        await update_post(post, data)


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


async def update_post(post:schemas.Post, data:dict):
    modified_post = post.copy()
    
    modified_post.upvotes = data['score']['up']
    modified_post.downvotes = data['score']['down']
    modified_post.source = get_source(data)
    modified_post.tags = get_tags(data, post.full.type)
    modified_post.source = get_source(data)

    if modified_post != post:
        database.Post.update(post.id, modified_post)



async def import_post(data:dict):
    full = construct_image(data['file'])
    preview = construct_image(data['sample'])
    thumbnail = construct_image(data['preview'])
    if full == None or thumbnail == None:
        raise ImportFailure("Failed to Generate Images from E621 Post")

    post = schemas.Post(
        id=database.Post.generate_id(),
        created_at=get_date(data['created_at']),
        media_type=utils.predict_media_type(data['file']['url']), # type: ignore
        full=full,
        preview=preview,
        thumbnail=thumbnail,
        tags=get_tags(data, full.type),
        source=get_source(data),
        upvotes=data['score']['up'],
        downvotes=data['score']['down'],
        hashes=schemas.Hashes(md5s=[data['file']['md5']]),
    )
    database.Post.insert(post)


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
