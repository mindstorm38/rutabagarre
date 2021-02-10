from entity import Entity, MotionEntity
from entity.incarnation import Incarnation
from entity.incarnation.farmer import Farmer
from enum import Enum, auto
import stage


class PlayerColor(Enum):
    """
    Enumeration of the colors available for the players
    """
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


class Player(MotionEntity):

    """
    Implementation of a player. Inherits from Entity
    """

    MOVE_VELOCITY = 0.04
    MOVE_AIR_FACTOR = 0.3
    JUMP_VELOCITY = 0.4

    def __init__(self, entity_stage: 'stage.Stage', number: int, color: PlayerColor, hp: float = 100.0) -> None:
        super().__init__(entity_stage)
        self._number: int = number
        self._color: PlayerColor = color
        self._hp: float = hp
        self._incarnation: Incarnation = Farmer()

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
        self.add_velocity(vel if self._on_ground else vel * self.MOVE_AIR_FACTOR, 0)

    def move_right(self) -> None:
        self._move_side(self.MOVE_VELOCITY)

    def move_left(self) -> None:
        self._move_side(-self.MOVE_VELOCITY)

    def move_jump(self) -> None:
        if self._on_ground:
            self.add_velocity(0, self.JUMP_VELOCITY)

    def attack_light(self) -> None:
        # We search for entities that will be hit
        hitbox_extended = self._cached_hitbox
        hitbox_extended.set_from(self.get_hitbox())
        hitbox_extended.expand(
            ((1, -1)[self.get_turned_to_left()]) * self._incarnation.get_light_attack_range(),
            0
        )
        players_hit = self.get_stage().foreach_colliding_entity(hitbox_extended, predicate=Player._is_player)
        for player_hit in players_hit:
            if player_hit != self:
                self._incarnation.attack_light(player_hit)

    def attack_heavy(self) -> None:
        # We search for entities that will be hit
        hitbox_extended = self._cached_hitbox
        hitbox_extended.set_from(self.get_hitbox())
        hitbox_extended.expand(
            ((1, -1)[self.get_turned_to_left()]) * self._incarnation.get_heavy_attack_range(),
            0
        )
        players_hit = self.get_stage().foreach_colliding_entity(hitbox_extended, predicate=Player._is_player)
        for player_hit in players_hit:
            if player_hit != self:
                self._incarnation.attack_heavy(player_hit)

    @staticmethod
    def _is_player(entity: Entity) -> bool:
        return isinstance(entity, Player)
