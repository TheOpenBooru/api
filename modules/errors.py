class UserViewableException(Exception):
    message:str
    
    def __init__(self, msg:str = "Unspecified Error"):
        self.message = msg

class ApplicationError(Exception): pass
