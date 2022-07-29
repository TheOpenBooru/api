from modules.database import User
from modules.account import auth

def delete(username:str):
    """Raises:
        KeyError: User Does Not Exist
    """
    if not User.existsByUsername("username"):
        raise KeyError("User Does Not Exist")
    else:
        user = User.getByUsername(username)
        User.delete(user.id)
        auth.delete(username)
