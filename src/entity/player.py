from typing import Tuple, cast, Optional, List, Iterable
from enum import Enum, auto
import random
import time

from entity.incarnation import Incarnation, Farmer, Potato
from entity import Entity, MotionEntity
from entity.effect import EffectType
import stage


class PlayerColor(Enum):
    """ Enumeration of the colors available for the players. """
    VIOLET = auto()
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
    YELLOW = auto()
    RED = auto()
    BROWN = auto()
    LIGHT_BLUE = auto()
    PINK = auto()
    LIGHT_BROWN = auto()
    LIGHT_ORANGE = auto()
    CHARTREUSE = auto()
    PALE_GREEN = auto()
    CYAN = auto()


class IncarnationType(Enum):
    """ Enumeration des """
    POTATO = auto()


class Player(MotionEntity):

    """
    Implementation of a player. Inherits from Entity
    """

    MOVE_VELOCITY = 0.04
    MOVE_AIR_FACTOR = 0.3
    JUMP_VELOCITY = 0.55

    INCARNATIONS_CONSTRUCTORS = {
        IncarnationType.POTATO: Potato
    }

    def __init__(self, entity_stage: 'stage.Stage', number: int, color: PlayerColor, hp: float = 100.0) -> None:

        super().__init__(entity_stage)

        self._number: int = number
        self._color: PlayerColor = color
        self._max_hp: float = hp
        self._hp: float = hp

        self._incarnation_type: Optional[IncarnationType] = None
        self._incarnation: Incarnation = Farmer(self)

        self._block_oves_until: float = 0.0
        self._block_action_until: float = 0.0
        self._invincible_until: float = 0.0
        self._sleeping: bool = False

        self._animations_queue: List[str] = []

    # GETTERS

    def get_number(self) -> int:
        return self._number

    def get_max_hp(self) -> float:
        return self._max_hp

    def get_hp(self) -> float:
        return self._hp

    def get_hp_ratio(self) -> float:
        return max(0.0, min(1.0, self._hp / self._max_hp))

    def get_color(self) -> PlayerColor:
        return self._color

    def get_incarnation(self) -> Incarnation:
        return self._incarnation

    def get_incarnation_type(self) -> IncarnationType:
        return self._incarnation_type

    def can_move(self) -> bool:
        return time.monotonic() >= self._block_oves_until

    def can_act(self) -> bool:
        return time.monotonic() >= self._block_action_until

    def is_invincible(self) -> bool:
        return self._sleeping or time.monotonic() < self._invincible_until

    def is_sleeping(self) -> bool:
        return self._sleeping

    # SETTERS

    def set_number(self, number: int) -> None:
        self._number = number

    def set_hp(self, hp: float) -> None:
        self._hp = hp

    def set_color(self, color: PlayerColor) -> None:
        self._color = color

    def set_incarnation(self, incarnation: Incarnation) -> None:
        self._incarnation = incarnation

    def block_moves_for(self, duration: float):
        self._block_oves_until = time.monotonic() + duration

    def block_action_for(self, duration: float):
        self._block_action_until = time.monotonic() + duration

    def set_invincible_for(self, duration: float):
        self._invincible_until = time.monotonic() + duration

    # ADDERS

    def add_to_hp(self, number) -> None:
        self._hp += number

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x - 0.5, y, x + 0.5, y + 2)

    # OTHER METHODS

    def update(self) -> None:
        super().update()
        if self._on_ground and self._vel_x != 0 and random.random() < 0.05:
            self._stage.add_effect(EffectType.SMALL_GROUND_DUST, 1, self._x, self._y)

    # MOVES

    def _move_side(self, vel) -> None:
        if self.can_move():
            self.add_velocity(vel if self._on_ground else vel * self.MOVE_AIR_FACTOR, 0)

    def move_right(self) -> None:
        self._move_side(self.MOVE_VELOCITY * self._incarnation.get_speed_multiplier())

    def move_left(self) -> None:
        self._move_side(-self.MOVE_VELOCITY * self._incarnation.get_speed_multiplier())

    def move_jump(self) -> None:
        # TODO: Si en train de dormir, sortir de terre.
        if self._on_ground and self.can_move():
            self.add_velocity(0, self.JUMP_VELOCITY)
            self._stage.add_effect(EffectType.BIG_GROUND_DUST, 1, self._x, self._y)

    def do_action(self) -> None:
        if self.can_act():
            self._incarnation.action()
            self.block_action_for(self._incarnation.get_action_cooldown())

    def do_heavy_action(self) -> None:
        if self.can_act():
            self._incarnation.heavy_action()
            self.block_action_for(self._incarnation.get_heavy_action_cooldown())

    def do_down_action(self) -> None:
        if (True,)[0]: # TODO: Y-a-t-il un joueur en dessous ?
            pass # TODO: Déterrer le joueur
        elif self._incarnation is not None:
            pass # TODO: S'enterrer s'il n'y a pas de joueur trop près

    # ACTIONS FOR INCARNATIONS

    def push_animation(self, anim: str):
        self._animations_queue.append(anim)

    def foreach_animation(self) -> Iterable[str]:
        for anim in self._animations_queue:
            yield anim
        self._animations_queue.clear()

    def poll_animation(self) -> Optional[str]:
        return self._animations_queue.pop(0) if len(self._animations_queue) else None

    def front_attack(self, reach: float, damage_range: Tuple[float, float], knockback: float):

        """
        Attack player in the reach range.
        :param reach: Reach range in the front of the player, negate the reach to indicate both side reach.
        :param damage_range: Range of damage to pick.
        :param knockback: Knockback multiplier
        """

        self._cached_hitbox.set_from(self._hitbox)
        if reach < 0:
            self._cached_hitbox.expand(reach, 0)
            self._cached_hitbox.expand(-reach, 0)
        else:
            reach_offset = self._hitbox.get_width() / 2
            reach = max(0, reach - reach_offset)
            self._cached_hitbox.expand(-reach if self.get_turned_to_left() else reach, 0)
            self._cached_hitbox.move(-reach_offset if self.get_turned_to_left() else reach_offset, 0)

        for target in self._stage.foreach_colliding_entity(self._cached_hitbox, predicate=Player.is_player):
            target = cast(Player, target)
            if target != self and not target.is_invincible():
                target.add_to_hp(-random.uniform(*damage_range) / target.get_incarnation().get_defense())
                knockback_x = random.uniform(0.1, 0.2) * knockback
                knockback_y = random.uniform(0.1, 0.3) * knockback
                if (reach < 0 and target.get_x() < self.get_x()) or (reach >= 0 and self.get_turned_to_left()):
                    knockback_x = -knockback_x
                target.add_velocity(knockback_x, knockback_y)
                target.push_animation("hit")

    @staticmethod
    def is_player(entity: Entity) -> bool:
        return isinstance(entity, Player)

    # INCARNATION

    def load_incarnation(self, typ: IncarnationType) -> bool:
        if self._incarnation_type is None and typ in self.INCARNATIONS_CONSTRUCTORS:
            constructor = self.INCARNATIONS_CONSTRUCTORS[typ]
            try:
                self._incarnation = constructor(self)
                self._incarnation_type = typ
                self.block_moves_for(1)
                self.block_action_for(1)
                self.set_invincible_for(1)
                self.push_animation("player:mutation")
                self._stage.add_effect(EffectType.SMOKE, 2, self._x, self._y)
                self._vel_x = 0
            except (Exception,):
                print("Error while constructing incarnation type {}.".format(typ.name))
                import traceback
                traceback.print_exc()
            return True
        else:
            return False