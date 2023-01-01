from openbooru.modules.database import User
from ..account import auth

def clear():
    User.clear()
    auth.clear()
