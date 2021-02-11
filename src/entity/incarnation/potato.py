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

    @staticmethod
    def get_action_cooldown() -> float:
        return 1.0

    def action(self):
        self._owner.front_attack(0, (5.0, 6.0), 0.6)
        self._owner.push_animation("potato:punch")

    def heavy_action(self):
        pass
