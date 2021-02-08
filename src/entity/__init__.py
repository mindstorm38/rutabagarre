from abc import ABC, abstractmethod
import stage


class Entity(ABC):

    def __init__(self, entity_stage: 'stage.Stage'):
        self._stage: 'stage.Stage' = entity_stage
        self._x: int = 0
        self._y: int = 0

    @abstractmethod
    def update(self): ...
