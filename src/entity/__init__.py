from abc import ABC, abstractmethod
import stage


class Entity(ABC):

    def __init__(self, entity_stage: 'stage.Stage'):
        self._stage = entity_stage
        self._x = 0
        self._y = 0

    @abstractmethod
    def update(self): ...
