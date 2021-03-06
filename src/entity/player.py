from typing import Tuple, cast, Optional, List, Iterable
from enum import Enum, auto
import random
import time

from entity.incarnation import Incarnation, Farmer, Potato, Corn, Carrot
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
    CORN = auto()
    CARROT = auto()


class Player(MotionEntity):

    """
    Implementation of a player. Inherits from Entity
    """

    MOVE_VELOCITY = 0.04
    MOVE_AIR_FACTOR = 0.3
    JUMP_VELOCITY = 0.65
    REGEN_BY_TICK = 0.1

    INCARNATIONS_CONSTRUCTORS = {
        IncarnationType.POTATO: Potato,
        IncarnationType.CORN: Corn,
        IncarnationType.CARROT: Carrot
    }

    def __init__(self, entity_stage: 'stage.Stage', player_index: int, color: PlayerColor, hp: float = 100.0) -> None:

        super().__init__(entity_stage)

        self._player_index: int = player_index
        self._color: PlayerColor = color
        self._max_hp: float = hp
        self._hp: float = hp

        self._incarnation_type: Optional[IncarnationType] = None
        self._incarnation: Incarnation = Farmer(self)
        self._incarnation_duration: float = 1.0  # = 1.0 pour éviter les div par 0
        self._incarnation_until: float = 0.0

        self._block_moves_until: float = 0.0
        self._block_action_until: float = 0.0
        self._block_heavy_action_until: float = 0.0
        self._block_jump_until: float = 0.0
        self._invincible_until: float = 0.0
        self._sleeping: bool = False

        self._special_action: bool = False
        self._special_action_reset_by_key: bool = False

        # (grabed player, grab at, throw at)
        self._grabing: Optional[Tuple['Player', float, float]] = None

        self._animations_queue: List[str] = []

        self._statistics = PlayerStatistics()

    # GETTERS

    def get_player_index(self) -> int:
        return self._player_index

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

    def has_incarnation(self) -> bool:
        return self._incarnation_type is not None

    def get_incarnation_duration_ratio(self) -> float:
        return max(0.0, (self._incarnation_until - (0 if self._sleeping else time.monotonic())) / self._incarnation_duration)

    def can_move(self) -> bool:
        return time.monotonic() >= self._block_moves_until and not self._sleeping

    def can_act(self) -> bool:
        return time.monotonic() >= self._block_action_until and not self._special_action and not self._sleeping

    def can_act_heavy(self) -> bool:
        return time.monotonic() >= self._block_heavy_action_until and not self._special_action and not self._sleeping

    def can_jump(self) -> bool:
        return time.monotonic() >= self._block_jump_until and not self._sleeping

    def is_purely_invincible(self) -> bool:
        return time.monotonic() < self._invincible_until

    def is_invincible(self) -> bool:
        return self._sleeping or self.is_purely_invincible()

    def is_sleeping(self) -> bool:
        return self._sleeping

    def is_in_special_action(self) -> bool:
        return self._special_action

    def get_statistics(self) -> 'PlayerStatistics':
        return self._statistics

    # SETTERS

    def set_number(self, number: int) -> None:
        self._player_index = number

    def set_hp(self, hp: float) -> None:
        self._hp = hp

    def set_color(self, color: PlayerColor) -> None:
        self._color = color

    def set_incarnation(self, incarnation: Incarnation) -> None:
        self._incarnation = incarnation

    def block_moves_for(self, duration: float):
        self._block_moves_until = time.monotonic() + duration

    def block_action_for(self, duration: float):
        self._block_action_until = time.monotonic() + duration

    def block_heavy_action_for(self, duration: float):
        self._block_heavy_action_until = time.monotonic() + duration

    def block_jump_for(self, duration: float):
        self._block_jump_until = time.monotonic() + duration

    def set_invincible_for(self, duration: float):
        self._invincible_until = time.monotonic() + duration

    def complete_stun_for(self, duration: float):
        self.block_moves_for(duration)
        self.block_action_for(duration)
        self.block_heavy_action_for(duration)
        self.block_jump_for(duration)
        self.set_invincible_for(duration)

    def set_special_action(self, special: bool, reset_by_key: bool = False):
        self._special_action = special
        self._special_action_reset_by_key = special and reset_by_key

    # ADDERS

    def add_to_hp(self, number) -> bool:
        self._hp += number
        if self._hp < 0:
            self._stage.add_effect(EffectType.SMOKE, 2, self._x, self._y)
            self.set_dead()
            return True
        else:
            return False

    def remove_hp_to_other(self, target: 'Player', hp: float):
        hp /= target.get_incarnation().get_defense()
        self._statistics.add_damage_dealt(int(hp))
        target._statistics.add_damage_taken(int(hp))
        if target.add_to_hp(-hp):
            self._statistics.add_kos(1)

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x - 0.5, y, x + 0.5, y + 2)

    # OTHER METHODS

    def update(self) -> None:

        super().update()

        if self._y < -10:
            self.set_hp(0)
            self.set_dead()
            return

        elif self._x < 1 or self._x > 29:
            self._stage.add_effect(EffectType.SMOKE, 1, self._x, self._y)
            self.set_hp(0)
            self.set_dead()

            return

        if self._on_ground and self._vel_x != 0 and random.random() < 0.05:
            self._stage.add_effect(EffectType.SMALL_GROUND_DUST, 1, self._x, self._y)

        if self._incarnation_type is not None and not self._sleeping and time.monotonic() >= self._incarnation_until:
            self._incarnation = Farmer(self)
            self._incarnation_type = None
            self._incarnation_duration = 1
            self.set_special_action(False)
            self.complete_stun_for(1)
            self.push_animation("player:unmutation")
            self._stage.add_effect(EffectType.SMOKE, 2, self._x, self._y)

        if self._special_action:
            self._incarnation.special_action()
        elif self._sleeping:
            if random.random() < 0.003:
                self._stage.add_effect(EffectType.SLEEPING, 5, self._x + random.uniform(-1, 1), self._y + 0.2 + random.random() * 0.6)
            if self._hp < self._max_hp:
                self._hp = min(self._hp + Player.REGEN_BY_TICK, self._max_hp)
        elif self._grabing is not None:
            target, grab_at, throw_at = self._grabing
            target = cast(Player, target)
            now = time.monotonic()
            if grab_at != 0:
                if now >= grab_at:
                    target.add_velocity(0, 0.5)
                    self._grabing = target, 0, throw_at
            elif now >= throw_at:
                knockback_x = random.uniform(0.1, 0.2)
                knockback_y = random.uniform(0.9, 1.1)
                target_on_left = target.get_x() < self.get_x()
                target.add_velocity(-knockback_x if target_on_left else knockback_x, knockback_y)
                target.push_animation("hit")
                target.set_invincible_for(0.5)
                self.remove_hp_to_other(target, random.uniform(17.0, 20.0))
                self._grabing = None

    # MOVES

    def _move_side(self, vel) -> None:
        if self.can_move():
            self.add_velocity(vel if self._on_ground else vel * self.MOVE_AIR_FACTOR, 0)

    def move_right(self) -> None:
        if self.get_turned_to_left() and self._special_action_reset_by_key:
            self.set_special_action(False)
        self._move_side(self.MOVE_VELOCITY * self._incarnation.get_speed_multiplier())

    def move_left(self) -> None:
        if not self.get_turned_to_left() and self._special_action_reset_by_key:
            self.set_special_action(False)
        self._move_side(-self.MOVE_VELOCITY * self._incarnation.get_speed_multiplier())

    def move_jump(self) -> None:
        if self._sleeping:
            self.set_sleeping(False)
            """self._sleeping = False
            self.complete_stun_for(0.6)
            # On restaure le temps restant
            self._incarnation_until += time.monotonic()"""
        elif self._on_ground and self.can_jump():
            self.add_velocity(0, self.JUMP_VELOCITY)
            self._stage.add_effect(EffectType.BIG_GROUND_DUST, 1, self._x, self._y)
            self.block_jump_for(0.05)

    def do_action(self) -> None:
        if self.can_act():
            self._incarnation.action()
            self.block_action_for(self._incarnation.get_action_cooldown())

    def do_heavy_action(self) -> None:
        if self.can_act_heavy():
            self._incarnation.heavy_action()
            self.block_heavy_action_for(self._incarnation.get_heavy_action_cooldown())

    def do_down_action(self) -> None:

        if not self.can_move() or self._grabing is not None or not self._on_ground:
            return

        can_sleep = self._incarnation_type is not None

        for target in self.foreach_down_sleeping_players():
            target = cast(Player, target)
            can_sleep = False
            if not target.is_purely_invincible():
                now = time.monotonic()
                self._grabing = (target, now + 0.5, now + 1)
                self.complete_stun_for(1)
                target.set_sleeping(False)
                target.complete_stun_for(1)
                # target._sleeping = False
                self.push_animation("grabing")
                return

        if can_sleep:
            self.set_sleeping(True)
            """self._sleeping = True
            # Quand on dors, on défini le "until" au temps restant, afin de le restaurer au reveil
            self._incarnation_until -= time.monotonic()
            self.set_invincible_for(2)"""

    # ACTIONS FOR INCARNATIONS

    def push_animation(self, anim: str):
        self._animations_queue.append(anim)

    def foreach_animation(self) -> Iterable[str]:
        for anim in self._animations_queue:
            yield anim
        self._animations_queue.clear()

    def poll_animation(self) -> Optional[str]:
        return self._animations_queue.pop(0) if len(self._animations_queue) else None

    def front_attack(self, reach: float, damage_range: Tuple[float, float], knockback_x: float, knockback_y: float, *, given_imune: float = 0.5):

        """
        Attack player in the reach range.
        :param reach: Reach range in the front of the player, negate the reach to indicate both side reach.
        :param damage_range: Range of damage to pick.
        :param knockback_x: Knockback multiplier x-axis
        :param knockback_y: Knockback multiplier y-axis
        :param given_imune: Invincibility to add to target.
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
                self.remove_hp_to_other(target, random.uniform(*damage_range))
                knockback_x = random.uniform(0.1, 0.2) * knockback_x
                knockback_y = random.uniform(0.1, 0.3) * knockback_y
                if (reach < 0 and target.get_x() < self.get_x()) or (reach >= 0 and self.get_turned_to_left()):
                    knockback_x = -knockback_x
                target.add_velocity(knockback_x, knockback_y)
                target.push_animation("hit")
                target.set_invincible_for(given_imune)

    def foreach_down_sleeping_players(self):

        # On réduit la boit de collision en haut du joueur pour ne pas pouvoir
        # dormir ou déterrer qqun si on est un peu plus haut que le joueur
        self._cached_hitbox.set_from(self._hitbox)
        self._cached_hitbox.set_min_y(self._cached_hitbox.get_max_y() - 0.2)

        for target in self._stage.foreach_colliding_entity(self._cached_hitbox, predicate=Player.is_sleeping_player):
            yield target

    def set_sleeping(self, sleeping: bool):
        if sleeping:
            self._sleeping = True
            # Quand on dors, on défini le "until" au temps restant, afin de le restaurer au reveil
            self._incarnation_until -= time.monotonic()
            self.set_invincible_for(1)
        else:
            self._sleeping = False
            # On restaure le temps restant
            self._incarnation_until += time.monotonic()
            self.complete_stun_for(0.6)

    @staticmethod
    def is_player(entity: Entity) -> bool:
        return isinstance(entity, Player)

    @staticmethod
    def is_sleeping_player(entity: Entity) -> bool:
        return isinstance(entity, Player) and entity.is_sleeping()

    # INCARNATION

    def load_incarnation(self, typ: IncarnationType) -> bool:
        if self._incarnation_type is None and typ in self.INCARNATIONS_CONSTRUCTORS:
            constructor = self.INCARNATIONS_CONSTRUCTORS[typ]
            try:
                self._incarnation = constructor(self)
                self._incarnation_type = typ
                self._incarnation_duration = self._incarnation.get_duration()
                self._incarnation_until = time.monotonic() + self._incarnation_duration
                self.set_special_action(False)
                self.complete_stun_for(1)
                self.push_animation("player:mutation")
                self._stage.add_effect(EffectType.SMOKE, 2, self._x, self._y)
                self._vel_x = 0
                self._statistics.add_plants_collected(1)
            except (Exception,):
                print("Error while constructing incarnation type {}.".format(typ.name))
                import traceback
                traceback.print_exc()
            return True
        else:
            return False


class PlayerStatistics:

    def __init__(self):

        self._kos: int = 0
        self._plants_collected: int = 0
        self._damage_dealt: int = 0
        self._damage_taken: int = 0

    def get_kos(self) -> int:
        return self._kos

    def get_plants_collected(self) -> int:
        return self._plants_collected

    def get_damage_dealt(self) -> int:
        return self._damage_dealt

    def get_damage_taken(self) -> int:
        return self._damage_taken

    def add_kos(self, ko: int):
        self._kos += ko

    def add_plants_collected(self, pl_co: int):
        self._plants_collected += pl_co

    def add_damage_dealt(self, da_de: int):
        self._damage_dealt += da_de

    def add_damage_taken(self, da_ta: int):
        self._damage_taken += da_ta
