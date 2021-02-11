from entity.incarnation import Incarnation
from entity.effect import EffectType
from entity import player
import random


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
        return 0.5

    @staticmethod
    def get_heavy_action_cooldown() -> float:
        return 4.0

    def action(self):
        self._owner.front_attack(0, (5.0, 6.0), 0.6, 0.6)
        self._owner.push_animation("potato:punch")

    def heavy_action(self):
        self._owner.set_special_action(True, True)
        self._owner.push_animation("potato:roll")

    def special_action(self):
        self._owner.set_velocity(-0.25 if self._owner.get_turned_to_left() else 0.25, self._owner.get_vel_y())
        self._owner.block_moves_for(0.5)
        self._owner.front_attack(0, (15.0, 16.0), -2, 2)
        if random.random() < 0.08:
            self._owner.get_stage().add_effect(EffectType.BIG_GROUND_DUST, 1, self._owner.get_x(), self._owner.get_y())
