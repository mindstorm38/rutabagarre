from entity.motion_entity import MotionEntity
from entity.motion_entity.incarnation import Incarnation
from entity.motion_entity.incarnation.farmer import Farmer
from enum import Enum, auto
import stage


class PlayerColor(Enum):
    """
    Enumeration of the colors available for the players
    """
    VIOLET = auto()
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
    YELLOW = auto()
    RED = auto()
    BLACK = auto()


class Player(MotionEntity):
    """
    Implementation of a player. Inherits from Entity
    """

    def __init__(self, entity_stage: 'stage.Stage', number: int, color: PlayerColor, hp: float = 100.0) -> None:
        super().__init__(entity_stage)
        self._number: int = number
        self._color: PlayerColor = color
        self._hp: float = hp
        self._incarnation: Incarnation = Farmer()

    # GETTERS
    def get_number(self) -> int:
        return self._number

    def get_hp(self) -> float:
        return self._hp

    def get_color(self) -> PlayerColor:
        return self._color

    def get_incarnation(self) -> Incarnation:
        return self._incarnation

    @staticmethod
    def get_hard_hitbox() -> bool:
        return False

    # SETTERS
    def set_number(self, number: int) -> None:
        self._number = number

    def set_hp(self, hp: float) -> None:
        self._hp = hp

    def set_color(self, color: PlayerColor) -> None:
        self._color = color

    def set_incarnation(self, incarnation: Incarnation) -> None:
        self._incarnation = incarnation

    # ADDERS
    def add_to_hp(self, number) -> None:
        self._hp += number

    # OTHER METHODS
    def update(self) -> None:
        ...  # TODO l'implémenter
