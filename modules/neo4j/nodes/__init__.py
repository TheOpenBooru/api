class Entry:
    @staticmethod
    def create(*args) -> int:
        """Create the Entry

        Parameters:
            *args (any): 

        Raises:
            KeyError: That Entry already exsted

        Returns:
            int: Returns the Entry's ID
        """
        raise NotImplementedError
    
    @staticmethod
    def get(id:int) -> dict:
        """Get the Entry via ID

        Parameters:
            ID (int): The Entry ID
        
        Raises:
            KeyError: Entry with that ID doesn't exist

        Returns:
            dict: Returns the Entry's contents and any implicit data (Relationships)
        """
        raise NotImplementedError
    
    @staticmethod
    def delete(id:int):
        """Delete the Entry via ID

        Parameters:
            ID (int): The Entry ID
        """
        raise NotImplementedError


from .. import utils,driver,measureTiming