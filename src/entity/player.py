from entity import Entity, MotionEntity
from entity.incarnation import Incarnation, Farmer, Potato
from typing import Tuple, cast, Optional, List, Iterable
from enum import Enum, auto
import random
import stage
import time


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
        self._hp: float = hp

        self._incarnation_type: Optional[IncarnationType] = None
        self._incarnation: Incarnation = Farmer(self)

        self._animations_queue: List[str] = []
        self._block_oves_until = 0

    # GETTERS

    def get_number(self) -> int:
        return self._number

    def get_hp(self) -> float:
        return self._hp

    def get_color(self) -> PlayerColor:
        return self._color

    def get_incarnation(self) -> Incarnation:
        return self._incarnation

    # SETTERS

    def set_number(self, number: int) -> None:
        self._number = number

    def set_hp(self, hp: float) -> None:
        self._hp = hp

    def set_color(self, color: PlayerColor) -> None:
        self._color = color

    def set_incarnation(self, incarnation: Incarnation) -> None:
        self._incarnation = incarnation

    # ADDERS

    def add_to_hp(self, number) -> None:
        self._hp += number

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x - 0.5, y, x + 0.5, y + 2)

    # OTHER METHODS

    def update(self) -> None:
        super().update()

    # MOVES

    def _move_side(self, vel) -> None:
        if self.can_move():
            self.add_velocity(vel if self._on_ground else vel * self.MOVE_AIR_FACTOR, 0)

    def move_right(self) -> None:
        self._move_side(self.MOVE_VELOCITY * self._incarnation.get_speed_multiplier())

    def move_left(self) -> None:
        self._move_side(-self.MOVE_VELOCITY * self._incarnation.get_speed_multiplier())

    def move_jump(self) -> None:
        if self._on_ground and self.can_move():
            self.add_velocity(0, self.JUMP_VELOCITY)

    def do_action(self) -> None:
        self._incarnation.action()

    def do_heavy_action(self) -> None:
        self._incarnation.heavy_action()

    # ACTIONS FOR INCARNATIONS

    def push_animation(self, action: str):
        self._animations_queue.append(action)

    def foreach_animation(self) -> Iterable[str]:
        for anim in self._animations_queue:
            yield anim
        self._animations_queue.clear()

    def poll_animation(self) -> Optional[str]:
        return self._animations_queue.pop(0) if len(self._animations_queue) else None

    def front_attack(self, reach: float, damage_range: Tuple[float, float]):

        """
        Attack player in the reach range.
        :param reach: Reach range in the front of the player, negate the reach to indicate both side reach.
        :param damage_range: Range of damage to pick.
        """

        self._cached_hitbox.set_from(self._hitbox)
        if reach < 0:
            self._cached_hitbox.expand(reach, 0)
            self._cached_hitbox.expand(-reach, 0)
        else:
            reach_offset = self._hitbox.get_width() / 2
            reach -= reach_offset
            self._cached_hitbox.expand(-reach if self.get_turned_to_left() else reach, 0)
            self._cached_hitbox.move(-reach_offset if self.get_turned_to_left() else reach_offset, 0)

        for target in self._stage.foreach_colliding_entity(self._cached_hitbox, predicate=Player.is_player):
            target = cast(Player, target)
            if target != self:
                target.add_to_hp(-random.uniform(*damage_range) / target.get_incarnation().get_defense())
                knockback_x = random.uniform(0.01, 0.03)
                target.add_velocity(-knockback_x if self.get_turned_to_left() else knockback_x, random.uniform(0.02, 0.05))

    def block_moves_for(self, duration: float):
        self._block_oves_until = time.monotonic() + duration

    def can_move(self) -> bool:
        return time.monotonic() >= self._block_oves_until

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
            except (Exception,):
                print("Error while constructing incarnation type {}.".format(typ.name))
                import traceback
                traceback.print_exc()
            return True
        else:
            return False