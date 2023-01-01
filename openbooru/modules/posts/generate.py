from openbooru.modules import (
    schemas,
    encoding,
    database,
    encoding,
    store,
    settings,
    phash,
    normalise,
    tags,
)
from openbooru.modules.tags import generate_ai_tags
from PIL.Image import Image
import base64
import mimetypes
import hashlib


async def generate(data: bytes, filename: str, uploader_id: int | None = None) -> schemas.Post:
    hashes = schemas.Hashes()
    with await encoding.generate_encoder(data, filename) as media:
        full = media.original()
        full_schema = process_file(full, hashes)

        preview = media.preview()
        preview_schema = process_file(preview, hashes) if preview else None

        thumbnail = media.thumbnail()
        thumbnail_schema = process_file(thumbnail, hashes)

    add_hashes(hashes, data)
    if isinstance(media, encoding.ImageEncoder):
        generate_phash(hashes, media.pillow)

    post = schemas.Post(
        id=database.Post.generate_id(),
        uploader=uploader_id,
        hashes=hashes,
        full=full_schema,
        preview=preview_schema,
        thumbnail=thumbnail_schema,  # type: ignore
    )
    post.protected_tags = generate_meta_tags(post)
    return post


def process_file(file: encoding.GenericFile, hashes: schemas.Hashes) -> schemas.Media:
    add_hashes(hashes, file.data)
    filename = generate_filename(file)
    save_file(file.data, filename)
    url = store.generate_generic_url(filename)
    schema = generate_schema(file, url)
    return schema


def save_file(data: bytes, filename: str):
    try:
        store.put(data, filename)
    except FileExistsError:
        store.delete(filename)
        store.put(data, filename)


def add_hashes(hashes: schemas.Hashes, data: bytes):
    md5 = hashlib.md5(data).digest()
    sha256 = hashlib.sha256(data).digest()
    hashes.md5s.append(md5)
    hashes.sha256s.append(sha256)


def generate_phash(hashes: schemas.Hashes, image: Image):
    p_hash = phash.hash(image)
    hashes.phashes.append(p_hash)


def generate_schema(file: encoding.GenericFile, url: str) -> schemas.Media:
    if isinstance(file, encoding.ImageFile):
        return schemas.Image(
            url=url,
            mimetype=file.mimetype,
            height=file.height,
            width=file.width,
        )
    elif isinstance(file, encoding.AnimationFile):
        return schemas.Animation(
            url=url,
            mimetype=file.mimetype,
            height=file.height,
            width=file.width,
            duration=file.duration,
            frame_count=file.frame_count,
        )
    elif isinstance(file, encoding.VideoFile):
        return schemas.Video(
            url=url,
            mimetype=file.mimetype,
            height=file.height,
            width=file.width,
            duration=file.duration,
            fps=file.framerate,
            has_sound=file.hasAudio,
        )
    else:
        raise TypeError("Unknown file type")


def generate_filename(file: encoding.GenericFile) -> str:
    hash_bytes = hashlib.sha3_256(file.data).digest()
    hash = base64.urlsafe_b64encode(hash_bytes).decode()
    hash = hash[:10]

    ext = mimetypes.guess_extension(file.mimetype) or ""
    filename = hash + ext
    return filename


def generate_meta_tags(post: schemas.Post) -> list[str]:
    tags = post.tags.copy()

    tags.append(post.full.type)
    if isinstance(post.full, schemas.Video) and post.full.has_sound:
        tags.append("sound")

    return tags
