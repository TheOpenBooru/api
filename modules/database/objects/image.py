from dataclasses import dataclass
from . import _db_run,_combine_kwargs,_isUnique,Validate

_DATA_QUERY = """
    RETURN 
        ID(n) as id,
        n.url as url,
        n.md5 as md5,
        n.height as height,
        n.width as width,
        n.mimetype as mimetype
"""

@dataclass(frozen=True)
class Image:
    id:int
    url:str
    md5:str
    height:int
    width:int
    mimetype:str


def create(url:str,md5:str,height:int,width:int,mimetype:str) -> Image:
    """Create a Image object

    Raises:
    - ValueError: Property is not valid
    - KeyError: Image with that MD5 or URL already exists
    """
    if not Validate.url(url):
        raise ValueError ("URL is not a valid md5")
    if not Validate.md5(md5):
        raise ValueError ("MD5 is not a valid md5")
    if not _isUnique.image(md5,url):
        raise KeyError("Image with that MD5 or URL already exists")
    query = """CREATE (n:Image {
            url:$url,
            md5:$md5,
            height:$height,
            width:$width,
            mimetype:$mimetype
        })"""
    query += _DATA_QUERY
    data = _db_run(
        query,
        url=url,md5=md5,height=height,width=width,mimetype=mimetype
    )
    return Image(**data[0])

def get(**kwargs):
    """Get an image from a property

    kwargs:
    - url: The URL for the image
    - md5: The MD5 hash for the image

    Raises:
        ValueError: A kwarg key is invalid
        TypeError: A kwarg was not of the correct type
        KeyError: No image was found with that property
    """
    if len(kwargs) != 1:
        raise ValueError("Invalid Kwargs Length")
    
    LOOKUP = {
        'url' : (str,"WHERE n.url = $url"),
        'md5' : (str,"WHERE n.md5 = $md5"),
    }
    
    query = "MATCH (n:Image)"
    query += _combine_kwargs(LOOKUP,kwargs)
    query += _DATA_QUERY
    data = _db_run(query,**kwargs)
    
    if not data:
        raise KeyError("No Image Found with that property")
    return Image(**data[0])

def set(id:int,**kwargs):
    """Set the values of an image object

    kwargs:
        - url (str): image url
        - md5 (str): image md5
        - height (int): image height
        - width (int): image width
        - mimetype (str): image mimetype

    Raises:
        - ValueErrror: A kwarg key is invalid
        - TypeError: A kwarg is not of the correct type
    """
    LOOKUP = {
        'url'      : (str,"SET n.url = $url"),
        'md5'      : (str,"SET n.md5 = $md5"),
        'width'    : (int,"SET n.width = $width"),
        'height'   : (int,"SET n.height = $height"),
        'mimetype' : (str,"SET n.mimetype = $mimetype"),
        }
    
    query = "MATCH (n:Image) WHERE ID(n) = $id"
    query += _combine_kwargs(LOOKUP,kwargs)
    query += _DATA_QUERY

    _db_run(query,id=id,**kwargs)

def delete(id:int):
    _db_run("""
            MATCH (n:Image)
                WHERE ID(n) = $id
            DETACH DELETE n""",
        id=id
    )
