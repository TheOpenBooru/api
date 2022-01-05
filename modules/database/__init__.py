import os
import enum
import neo4j as _neo

class User_Level(enum.IntEnum):
    TEMPORARY = 0
    USER = 10
    ADMIN = 50
    OWNER = 100

_driver:_neo.BoltDriver =_neo.GraphDatabase.driver(
    os.getenv('NEO_URI'),
    auth=(os.getenv('NEO_USER'),os.getenv('NEO_PASS')),
    connection_acquisition_timeout=5,
    connection_timeout=3
    ) # type: ignore


from .utils import db_run,clear,isUnique
from ..validation import isValid
from .Objects import Post,Tag,User,Image