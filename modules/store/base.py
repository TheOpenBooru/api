class BaseStore:
    local:bool = False
    usable:bool = False
    fail_reason:str = "No Reason"
    def __init__(self):
        ...
    
    def put(self, data: bytes, filename:str):
        """Store a file as the specified filename
        
        Raises:
        - TypeError: The data wasn't bytes
        - FileExistsError: The file already exists
        """
        raise NotImplementedError


    def exists(self, filename:str) -> bool:
        "Checks if a file exists"
        raise NotImplementedError

    
    def get(self, filename:str) -> bytes:
        """Retrieves the data from a file stored
        
        Raises:
        - FileNotFoundError: Could not find a file with that name
        """
        raise NotImplementedError
    

    def url(self, filename:str) -> str:
        """Generates the URL for the file"""
        raise NotImplementedError
    

    def delete(self, filename:str):
        "Deletes a file with the specified filename"
        raise NotImplementedError
    

    def clear(self):
        "Deletes every file stored"
        raise NotImplementedError
