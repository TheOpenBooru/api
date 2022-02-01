from ..types import Image
import random

_images = {}

def create(url:str,height:int,width:int,mimetype:str) -> int:
    id = random.randint(0,2**64)
    img = Image(
        id=len(_images),
        url=url,mimetype=mimetype,
        height=height,width=width,
    )
    _images[id] = img
    return id

def get(id:int):
    """Raises:
        - KeyError: No post with that ID
    """
    return _images[id]

def delete(id:int):
    _images.pop(id)