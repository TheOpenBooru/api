from ._database import db
from . import Post, Tag, User, Subscriptions

def clear():
    Post.clear()
    User.clear()
    Tag.clear()