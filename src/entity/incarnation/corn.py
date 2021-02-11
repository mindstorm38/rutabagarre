from entity.incarnation import Incarnation
from entity.bullet import Bullet
from entity import player
import random
import time


class Corn(Incarnation):

    """
    Implementation of the incarnation Corn, the range attacker. Inherits from incarnation
    """

    def __init__(self, owner_player: 'player.Player'):
        super().__init__(owner_player)
        self._remaining_bullets: int = 0
        self._next_shot_time: float = 0.0
        self._shot_interval: float = 0.0

    # GETTER

    @staticmethod
    def get_duration() -> float:
        return 25

    @staticmethod
    def get_name() -> str:
        return "corn"

    @staticmethod
    def get_defense() -> float:
        return 0.5

    @staticmethod
    def get_speed_multiplier() -> float:
        return 1.2

    @staticmethod
    def get_action_cooldown() -> float:
        return 5.0

    @staticmethod
    def get_heavy_action_cooldown() -> float:
        return 10.0

    def action(self):
        # self._owner.push_animation("corn:shot")
        self._remaining_bullets = 10
        self._next_shot_time = time.monotonic() + 0.4
        self._shot_interval = 0.2
        self._owner.set_special_action(True)

    def heavy_action(self):
        # self._owner.push_animation("corn:shot")
        self._remaining_bullets = 30
        self._next_shot_time = time.monotonic() + 0.4
        self._shot_interval = 0.05
        self._owner.set_special_action(True)

    def special_action(self):

        if self._remaining_bullets > 0:
            if self._next_shot_time == 0 or time.monotonic() >= self._next_shot_time:
                dx = -0.4 if self._owner.get_turned_to_left() else 0.4
                pos_x = -0.5 if self._owner.get_turned_to_left() else 0.5
                bullet = self._owner.get_stage().add_entity(Bullet, self._owner, random.uniform(1.0, 1.2), dx)
                bullet.set_position(self._owner.get_x() + pos_x, self._owner.get_y() + 0.8)
                self._remaining_bullets -= 1
                self._next_shot_time = time.monotonic() + self._shot_interval

        if self._remaining_bullets <= 0:
            self._owner.set_special_action(False)

