from abc import ABC, abstractmethod
from entity import player


class Incarnation(ABC):
    def __init__(self) -> None:
        self._duration: float = 10.0

    # GETTERS
    def get_duration(self) -> float:
        return self._duration

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @staticmethod
    def get_attack() -> float:
        return 1.0

    @staticmethod
    def get_defense() -> float:
        return 1.0

    @staticmethod
    def get_speed_multiplier() -> float:
        return 1.0

    # SETTERS
    def set_duration(self, duration: float) -> None:
        self._duration = duration

    # ADDERS
    def add_to_duration(self, number: float) -> None:
        self._duration += number

    # OTHER METHODS
    def attack_light(self, target: 'player.Player') -> None:
        target.add_to_hp(- (self.get_attack() - target.get_incarnation().get_defense()))

    def attack_heavy(self, target: 'player.Player') -> None:
        target.add_to_hp(- (self.get_attack() - target.get_incarnation().get_defense() / 2))
