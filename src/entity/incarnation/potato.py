from entity.incarnation import Incarnation
from entity import player


class Potato(Incarnation):
    """
    Implementation of the incarnation Potato, the solid attacker. Inherits from incarnation
    """
    def __init__(self, owner_player: 'player.Player'):
        Incarnation.__init__(self, owner_player)

    # GETTER
    @staticmethod
    def get_name() -> str:
        return "potato"

    @staticmethod
    def get_defense() -> float:
        return 1.5

    @staticmethod
    def get_speed_multiplier() -> float:
        return 0.7
