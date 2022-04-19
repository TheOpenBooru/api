_posts_store = {}

from modules.schemas import Post
from .validation import is_post_unique,is_post_valid
from .misc import all,clear,get_unused_id
from .get import get
from .create import create
from .delete import delete,restore
from .search import search
from .update import update
from .actions import increment_view