from entity.incarnation import Incarnation
from entity.bullet import Bullet
from entity import player
import random


class Corn(Incarnation):

    """
    Implementation of the incarnation Corn, the range attacker. Inherits from incarnation
    """

    def __init__(self, owner_player: 'player.Player'):
        super().__init__(owner_player)
        self._remaining_bullets = 0

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

    def action(self):
        # self._owner.push_animation("corn:shot")
        self._remaining_bullets = 6
        self._owner.set_special_action(True)

    def heavy_action(self):
        # self._owner.push_animation("corn:shot")
        self._remaining_bullets = 30
        self._owner.set_special_action(True)

    def special_action(self):

        if self._remaining_bullets > 0:
            dx = -3 if self._owner.get_turned_to_left() else 3
            pos_x = -0.5 if self._owner.get_turned_to_left() else 0.5
            bullet = self._owner.get_stage().add_entity(Bullet, self._owner, random.uniform(0.2, 0.3), dx)
            bullet.set_position(self._owner.get_x() + pos_x, self._owner.get_y() + 0.5)

        if self._remaining_bullets <= 0:
            self._owner.set_special_action(False)

