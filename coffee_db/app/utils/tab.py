from abc import ABC, abstractmethod


class Tab(ABC):

    @property
    @abstractmethod
    def header(self):
        return "default header"

    @abstractmethod
    def write(self):
        pass
