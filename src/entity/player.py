from . import Entity
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


class Player(Entity):
    """
    Implementation of a player. Inherits from Entity
    """

    def __init__(self, entity_stage: 'stage.Stage', number: int, color: PlayerColor, hp: int = 100) -> None:
        super().__init__(entity_stage)
        self._number: int = number
        self._color: PlayerColor = color
        self._hp: int = hp


    def update(self) -> None:
        ...  # TODO l'implémenter
