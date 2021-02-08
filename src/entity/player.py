from . import Entity
from src.entity.player_color import PlayerColor
import stage


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
