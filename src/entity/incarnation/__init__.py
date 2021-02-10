from abc import ABC, abstractmethod
from entity import player
from time import time


class Incarnation(ABC):

    def __init__(self, owner_player: 'player.Player') -> None:
        self._owner = owner_player
        self._end_time: float = time() + self.get_duration()

    # GETTERS
    @staticmethod
    def get_duration() -> float:
        return 10.0

    def get_end_time(self) -> float:
        return self._end_time

    @staticmethod
    def get_defense() -> float:
        return 1.0

    @staticmethod
    def get_speed_multiplier() -> float:
        return 1.0

    @staticmethod
    @abstractmethod
    def get_name() -> str: ...

    @abstractmethod
    def action(self): ...

    @abstractmethod
    def heavy_action(self): ...
