from entity.incarnation import Incarnation
from entity import player
from time import monotonic


class Carrot(Incarnation):

    """
    Implementation of the incarnation Carrot, the epeeist. Inherits from incarnation
    """
    COOLDOWN_THRUST = 0.4
    NUMBER_THRUST = 9

    def __init__(self, owner_player: 'player.Player'):
        Incarnation.__init__(self, owner_player)
        self._remaining_thrusts: int = 0
        self._next_thrust_time: float = 0

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
        return 8.0

    def action(self):
        self._owner.front_attack(0.3, (10.0, 12.0), 0.2, 0.2)
        self._owner.push_animation("carrot:strike")

    def heavy_action(self):
        self._remaining_thrusts = Carrot.NUMBER_THRUST
        self._next_thrust_time = monotonic() + 0.4
        self._owner.set_special_action(True, False)
        self._owner.block_moves_for(Carrot.COOLDOWN_THRUST * Carrot.NUMBER_THRUST)

    def special_action(self):
        if self._remaining_thrusts > 0 and self._next_thrust_time <= monotonic():
            if self._remaining_thrusts == 1:
                self._owner.front_attack(0.5, (15, 17), 2, 2, given_imune=0.0)
            else:
                self._owner.front_attack(0.5, (10, 12), 0, 0, given_imune=0.0)
                self._next_thrust_time = monotonic() + Carrot.COOLDOWN_THRUST
            self._remaining_thrusts -= 1

        if self._remaining_thrusts <= 0:
            self._owner.set_special_action(False)
