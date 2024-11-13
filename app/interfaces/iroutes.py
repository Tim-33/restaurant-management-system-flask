from abc import ABC, abstractmethod

class IRoutes(ABC):
    @abstractmethod
    def register_routes(self):
        pass