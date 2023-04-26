from abc import ABC, abstractmethod
from typing import Any


class ReleaseDestination(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def validate_destination(self):
        pass