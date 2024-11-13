from abc import ABC, abstractmethod

class IController(ABC):
    @abstractmethod
    def register_routes(self):
        pass