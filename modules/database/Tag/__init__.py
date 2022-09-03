from modules.schemas import Tag
from .. import db
from ._collection import tag_collection
from .misc import parse_doc, parse_docs

from .exists import exists
from .clear import clear
from .get import get
from .all import all
from .search import search
from .update import update
from .create import create
from .delete import delete
from .regenerate import regenerateCount
from .sibling import addSibling,removeSibling
