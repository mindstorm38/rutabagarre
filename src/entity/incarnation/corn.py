from entity.incarnation import Incarnation
from entity import player


class Corn(Incarnation):
    """
    Implementation of the incarnation Corn, the range attacker. Inherits from incarnation
    """
    def __init__(self, owner_player: 'player.Player'):
        Incarnation.__init__(self, owner_player)

    # GETTER
    @staticmethod
    def get_name() -> str:
        return "corn"

    @staticmethod
    def get_defense() -> float:
        return 0.5

    @staticmethod
    def get_speed_multiplier() -> float:
        return 1.2
