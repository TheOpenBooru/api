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

def create(url:str,md5:str,height:int,width:int,mimetype:str) -> int:
    """Create a Image object

    Raises:
    - ValueError
    - KeyError
    """
    if not Validate.md5(md5):
        raise ValueError ("MD% is not a valid md5")
    query = _db_run("""
        CREATE (n:Image {
            url:$url,
            md5:$md5,
            height:$height,
            width:$width,
            mimetype:$mime
        })
        RETURN ID(n)
        """,
        url=url,md5=md5,height=height,width=width,mime=mimetype
    )
    
    return query[0]['ID(n)']

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
    return data[0]

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