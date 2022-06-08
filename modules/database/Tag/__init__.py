from modules.schemas import Tag
from .. import db
from ._collection import tag_collection

from .exists import exists
from .get import get
from .all import all
from .search import search
from .create import create
from .regenerate import regenerate
