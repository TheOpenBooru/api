from openbooru.modules.errors import UserViewableException
class PostExistsException(Exception): pass
class PostEditFailure(UserViewableException): pass
class PostImportFailure(UserViewableException): pass