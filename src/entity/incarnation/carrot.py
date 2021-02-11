from entity.incarnation import Incarnation
from entity import player


class Carrot(Incarnation):

    """
    Implementation of the incarnation Carrot, the epeeist. Inherits from incarnation
    """

    def __init__(self, owner_player: 'player.Player'):
        Incarnation.__init__(self, owner_player)

    # GETTER
    @staticmethod
    def get_name() -> str:
        return "carrot"

    @staticmethod
    def get_defense() -> float:
        return 0.5

    @staticmethod
    def get_action_cooldown() -> float:
        return 0.5

    @staticmethod
    def get_heavy_action_cooldown() -> float:
        return 4.0

    def action(self):
        self._owner.front_attack(0.3, (10.0, 12.0), 0.2, 0.2)
        self._owner.push_animation("carrot:strike")

    def heavy_action(self):
        # TODO : la faire attaquer
        self._owner.push_animation("carrot:thrust")
