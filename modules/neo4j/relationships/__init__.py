"""Rules for relationship creation:

1. Only Node.add needs to be implemented
2. There should only be one relationship between two nodes
3. IDs are internal ids only
"""

from typing import List


class Relationship:
    @staticmethod
    def add(a:int,b:int):
        """Created a relationship from Node A to Node B
        
        Raises:
            TypeError: a or b arn't intergers IDs
        
        Args:
            a (int): Origin Node ID
            b (int): Connected Node ID
        """
        raise NotImplementedError

    def get(a:int=None,b:int=None) -> List[dict]:
        """Get's all relationships of this type connected to this ndoe

        Args:
            a (int, optional): Origin Node ID
            b (int, optional): Destination Node ID
        Raises:
            ValueError: No
        Returns:
            List[dict]: A list of relationships
        """
        raise NotImplementedError
    
    def remove(a:int,b:int):
        """Delete the relationship between Node A and Node B

        Args:
            a (int): Origin Node ID
            b (int): Connected Node ID

        Raises:
            NotImplementedError: This Relationship does not support deletion
        """
        raise NotImplementedError

from .. import driver