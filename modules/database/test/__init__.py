import os
import random
import string
from .. import User,Image,Post,Tag,clear

os.environ["DEPLOYMENT"] = "TESTING"

class LOOKUP:
    USER = {
        'id':int,
        'created_at':int,
        'avatar':dict,
        'name':str,
        'level':str,
        'description':str,
        'posts':list,
        'comments':list,
        'private':dict
    }
    IMAGE = {
        'id':int,
        'url':str,
        'width':int,
        'height':int,
        'md5':str,
        'mimetype':str
    }
    POST = {
        "id":int,
        "created_at":int,
        "type": str,
        "sound": bool,
        "source": str,
        "rating": str,
        "views": int,
        "upvotes": int,
        "downvotes": int,
        "tags": list,
        "comments": list,
        "annotations": list,
        "full": dict,
        "preview": dict,
        "thumbnail": dict,
    }

class DATA:
    USER = {
        'name':'example_user',
        'email':'example@example.com'
    }
    IMAGE = {
        "url": "https://example.com/image.jpeg",
        "md5": 'f'*32,
        "height": 1000,
        "width": 1000,
        "mimetype": "image/jpeg",
    }
    POST = {
        "type": "image",
        "sound": False,
        "source": "https://example.com/image.jpeg",
        "rating": "safe",
    }
