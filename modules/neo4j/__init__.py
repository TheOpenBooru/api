import os as _os
import neo4j as _neo
from neo4j import GraphDatabase as _GD,BoltDriver as _BD

driver:_BD = _GD.driver(_os.getenv('NEO_URI'),
            auth=(_os.getenv('NEO_USER'),_os.getenv('NEO_PASS')))


from .nodes.Tag import Tag
from .nodes.User import User
from .nodes.Post import Post

from .relationships.post_created import CreatedPost
from .relationships.tag_parent import ParentTag
from .relationships.tag_sibling import SiblingTag
from .relationships.tagged import Tagged
from .relationships.view import View

from . import utils,recommendation,maintenance