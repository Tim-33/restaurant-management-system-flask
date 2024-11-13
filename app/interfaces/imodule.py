from abc import ABC, abstractmethod

class IModule(ABC):
    @abstractmethod
    def register_blueprints(self):
        pass
