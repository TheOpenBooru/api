from . import GenericFile
from modules import schemas
from abc import ABC, abstractmethod


class BaseEncoder(ABC):
    type: schemas.MediaType

    def __init__(self, data: bytes):
        """Raises:
        - ValueError: Could not Parse Data
        """

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        pass

    @abstractmethod
    def original(self) -> GenericFile:
        """Raises:
        - FileNotFoundError: Didn't use with statement to create file
        """
        ...

    @abstractmethod
    def preview(self) -> GenericFile | None:
        """Raises:
        - FileNotFoundError: Didn't use with statement to create file
        """
        ...

    @abstractmethod
    def thumbnail(self) -> GenericFile:
        """Raises:
        - FileNotFoundError: Didn't use with statement to create file
        """
        ...
