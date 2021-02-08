from abc import ABC, abstractmethod
import stage


class Entity(ABC):

    def __init__(self, entity_stage: 'stage.Stage'):
        self._stage: 'stage.Stage' = entity_stage
        self._x: float = 0.0
        self._y: float = 0.0

    # GETTERS
    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_stage(self) -> 'stage.Stage':
        return self._stage

    # SETTERS
    def set_x(self, x: float) -> None:
        self._x = x

    def set_y(self, y: float) -> None:
        self._y = y

    def set_stage(self, stage: 'stage.Stage') -> None:
        self._stage = stage

    # ADDERS
    def add_to_x(self, number: float) -> None:
        self._x += number

    def add_to_y(self, number: float) -> None:
        self._y += number


    @abstractmethod
    def update(self): ...
