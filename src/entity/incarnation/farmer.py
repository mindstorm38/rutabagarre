from entity.incarnation import Incarnation
from entity import player


class Farmer(Incarnation):

    """
    Implementation of the incarnation Farmer, the classic incarnation. Inherits from incarnation
    """

    def __init__(self, owner_player: 'player.Player') -> None:
        super().__init__(owner_player)

    # GETTER

    @staticmethod
    def get_name() -> str:
        return "farmer"

    def action(self):
        self._owner.front_attack(1.0, (3.0, 5.0))

    def heavy_action(self):
        self._owner.front_attack(-1, (10.0, 12.0))

    def add_to_duration(self, number: float) -> None:
        """
        since the time in farmer is infinite, it's useless to change it
        """
        var = None
