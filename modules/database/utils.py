from . import objects as _objects

def clear():
    _objects.Post._posts_store = {}
    _objects.User._users_store = {}
    _objects.Tag._tags = {}


class isUnique:
    @staticmethod
    def user_name(name:str) -> bool:
        raise NotImplementedError

    @staticmethod
    def user_email(email:str) -> bool:
        raise NotImplementedError

    @staticmethod
    def image(md5:str,url:str) -> bool:
        raise NotImplementedError
