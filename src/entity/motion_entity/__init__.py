from abc import ABC
from src.entity import Entity
import stage


class MotionEntity(Entity, ABC):
    """
    Abstract subclass of Entity that can move
    """
    def __init__(self, entity_stage: 'stage.Stage') -> None:
        Entity.__init__(self, entity_stage)
        self._vel_x: float = 0.0
        self._vel_y: float = 0.0

    # GETTERS
    def get_vel_x(self) -> float:
        return self._vel_x

    def get_vel_y(self) -> float:
        return self._vel_y

    # SETTERS
    def set_vel_x(self, x: float) -> None:
        self._vel_x = x

    def set_vel_y(self, y: float) -> None:
        self._vel_y = y

    # ADDERS
    def add_vel_x(self, number: float) -> None:
        self._vel_x += number

    def add_vel_y(self, number: float) -> None:
        self._vel_y += number

