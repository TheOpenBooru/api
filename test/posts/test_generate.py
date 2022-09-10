from . import TEST_ANIMATION, TEST_IMAGE, TEST_VIDEO, TESTDATA
from modules import schemas, posts
import pytest
from pathlib import Path


async def generate_post(file:str) -> schemas.Post:
    path = Path(file)
    data = path.read_bytes()
    filename = path.name
    post = await posts.generate(data,filename)
    return post


@pytest.mark.asyncio
async def test_Post_Creation_Adds_Video_Tag():
    post = await generate_post(TEST_VIDEO['file'])
    assert 'video' in post.tags


@pytest.mark.asyncio
async def test_Post_Creation_Adds_Image_Tag():
    post = await generate_post(TEST_IMAGE['file'])
    assert 'image' in post.tags


@pytest.mark.asyncio
async def test_Post_Creation_Adds_Animation_Tag():
    post = await generate_post(TEST_ANIMATION['file'])
    assert 'animation' in post.tags


@pytest.mark.asyncio
async def test_image():
    attrs = TESTDATA["image"]["Complex"]
    data,filepath = load_testdata(attrs)
    post_obj = await posts.generate(data,filepath)
    
    assert post_obj.media_type == "image"
    assert isinstance(post_obj.full,schemas.Image)
    assert isinstance(post_obj.thumbnail,schemas.Image)
    assert_attributes(post_obj,attrs)


@pytest.mark.asyncio
async def test_animation():
    attrs = TESTDATA["animation"]["FractalGIF"]
    data,filepath = load_testdata(attrs)
    post_obj = await posts.generate(data,filepath)
    
    assert post_obj.media_type == "animation"
    assert isinstance(post_obj.full,schemas.Animation)
    assert isinstance(post_obj.thumbnail,schemas.Image)
    assert_attributes(post_obj,attrs)


@pytest.mark.asyncio
async def test_video():
    attrs = TESTDATA["video"]["heavy"]
    data,filepath = load_testdata(attrs)
    post_obj = await posts.generate(data,filepath)
    
    assert post_obj.media_type == "video"
    assert isinstance(post_obj.full,schemas.Video)
    assert isinstance(post_obj.thumbnail,schemas.Image)
    assert_attributes(post_obj,attrs)


def load_testdata(attrs:dict) -> tuple[bytes,str]:
    filepath = attrs['file']
    attrs.pop('file')
    with open(filepath,'rb') as f:
        data = f.read()
    return data,filepath


def assert_attributes(post:schemas.Post,attrs:dict):
    assert post.full.width == attrs["width"],f'{post.full.width} != {attrs["width"]}'
    assert post.full.height == attrs["height"],f'{post.full.height} != {attrs["height"]}'
    if isinstance(post.full, schemas.Video):
        assert post.full.duration == pytest.approx(attrs["duration"],rel=0.01)
        assert post.full.fps == attrs["framerate"]
        assert post.full.has_sound == attrs["hasAudio"]
