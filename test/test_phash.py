from modules import phash
from PIL import Image
import pytest


@pytest.fixture
def sample_image() -> Image.Image:
    return Image.open("data/test/image/Landscape.webp")


@pytest.fixture
def duplicate_images() -> tuple[Image.Image, Image.Image]:
    return (
        Image.open("data/test/duplicate/duplicate_a.jpg"),
        Image.open("data/test/duplicate/duplicate_b.jpg"),
    )


def test_Phash_Returns_Correct_Type(sample_image):
    hash = phash.phash(sample_image)
    assert type(hash) == bytes
    assert len(hash) == 8


def test_PHash_Matches_Similar_Images(duplicate_images, sample_image):
    image_a, image_b = duplicate_images
    image_c = sample_image
    
    hash_a = phash.phash(image_a)
    hash_b = phash.phash(image_b)
    hash_c = phash.phash(image_c)
    
    assert hash_a == hash_b
    assert hash_a != hash_c
