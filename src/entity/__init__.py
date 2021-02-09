from abc import ABC, abstractmethod
from entity.hitbox import Hitbox
import stage


class Entity(ABC):

    def __init__(self, entity_stage: 'stage.Stage'):
        self._stage: 'stage.Stage' = entity_stage
        self._x: float = 0.0
        self._y: float = 0.0
        self._hitbox = Hitbox(0, 0, 0, 0)

    # GETTERS
    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_stage(self) -> 'stage.Stage':
        return self._stage

    def get_hitbox(self) -> Hitbox:
        return self._hitbox

    @staticmethod
    def get_hard_hitbox() -> bool:
        return True

    # SETTERS
    def set_x(self, x: float) -> None:
        self._x = x

    def set_y(self, y: float) -> None:
        self._y = y

    def set_stage(self, stage_to_set: 'stage.Stage') -> None:
        self._stage = stage_to_set

    def set_hitbox(self, the_hitbox: Hitbox) -> None:
        self._hitbox = the_hitbox

    # ADDERS
    def add_to_x(self, number: float) -> None:
        self._x += number

    def add_to_y(self, number: float) -> None:
        self._y += number

    @abstractmethod
    def update(self): ...
