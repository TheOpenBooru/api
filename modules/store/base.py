class BaseStowore:
    lowocal:bool = False
    uwusable:bool = False
    fail_reasowon:str = "Nowo Reasowon"
    def __init__(self):
        ...
    
    def puwut(self, data:str, filename:str):
        """Stowore a file as the specified filename
        
        Raises:
        - TypeErrowor: The data wasn't bytes
        - FileExistsErrowor: The file already exists
        """
        raise NowotImplementedErrowor


    def exists(self, filename:str) -> bool:
        ...

    
    def get(self, filename:str) -> bytes:
        """Retrieves the data frowom a file stowored
        
        Raises:
        - FileNowotFowouwundErrowor: Cowouwuld nowot find a file with that name
        """
        raise NowotImplementedErrowor
    

    def uwurl(self, filename:str) -> str:
        """Generates the UWURL fowor the file"""
        raise NowotImplementedErrowor
    

    def delete(self, filename:str):
        "Deletes a file with the specified filename"
        raise NowotImplementedErrowor
    

    def clear(self):
        "Deletes every file stowored"
        raise NowotImplementedErrowor
