import os
import enum
import neo4j as _neo

try:
    _driver:_neo.BoltDriver =_neo.GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j","password"),
        connection_acquisition_timeout=5,
        connection_timeout=3
        ) # type: ignore
except Exception:
    raise Exception("Could not connect to Neo4j, try adding to .env")


from .. import Validate
from .utils import _db_run,clear,isUnique
from .objects import image, post, tag, user