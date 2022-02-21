from . import Post as _Post,Tag as _Tag,User as _User

def clear():
    _Post._posts_store = {}
    _User._users_store = {}
    _Tag._tags = {}


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
