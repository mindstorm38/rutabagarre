from abc import ABC, abstractmethod
from typing import List

from entity.hitbox import Hitbox
import stage


UID_COUNTER = 0
def new_uid() -> int:
    global UID_COUNTER
    UID_COUNTER += 1
    return UID_COUNTER


class Entity(ABC):

    def __init__(self, entity_stage: 'stage.Stage'):

        self._uid = new_uid()

        self._stage: 'stage.Stage' = entity_stage
        self._x: float = 0.0
        self._y: float = 0.0
        self._hitbox = Hitbox(0, 0, 0, 0)


    # GETTERS

    def get_uid(self) -> int:
        return self._uid
    
    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_stage(self) -> 'stage.Stage':
        return self._stage

    def get_hitbox(self) -> Hitbox:
        return self._hitbox

    @classmethod
    def has_hard_hitbox(cls) -> bool:
        return False

    # SETTERS

    def set_position(self, x: float, y: float):
        self._x = x
        self._y = y
        self._setup_box_pos(x, y)

    def move_position(self, dx: float, dy: float):
        self._hitbox.move(dx, dy)
        self._reset_pos_to_box()

    # Physics

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x, y, x, y)

    def _reset_pos_to_box(self):
        self._x = self._hitbox.get_mid_x()
        self._y = self._hitbox.get_min_y()

    @abstractmethod
    def update(self): ...


class MotionEntity(Entity, ABC):
    """
    Abstract subclass of Entity that can move
    """
    NATURAL_FRICTION = 0.95
    NATURAL_GRAVITY = 0.02

    def __init__(self, entity_stage: 'stage.Stage') -> None:

        super().__init__(entity_stage)

        self._vel_x: float = 0.0
        self._vel_y: float = 0.0

        self._cached_hitbox = Hitbox(0, 0, 0, 0)
        self._cached_hitboxes: List[Hitbox] = []

    # GETTERS

    def get_vel_x(self) -> float:
        return self._vel_x

    def get_vel_y(self) -> float:
        return self._vel_y

    # SETTERS

    def set_velocity(self, dx: float, dy: float):
        self._vel_x = dx
        self._vel_y = dy

    def add_velocity(self, ddx: float, ddy: float):
        self._vel_x += ddx
        self._vel_y += ddy

    # OTHER METHODS

    def update(self) -> None:
        self.update_motion()

    def update_motion(self) -> None:
        self.update_natural_velocity()
        self.move_position(self._vel_x, self._vel_y)

    def update_natural_velocity(self) -> None:
        self._vel_x *= MotionEntity.NATURAL_FRICTION
        self._vel_y = self._vel_y * MotionEntity.NATURAL_FRICTION - MotionEntity.NATURAL_GRAVITY

    @staticmethod
    def _has_entity_hard_box(entity: Entity) -> bool:
        return entity.has_hard_hitbox()

    def move_position(self, dx: float, dy: float) -> None:
        """
        Moves the entity and its hitbox following its actual velocity,
        taking care of other hitboxes onto the stage
        """

        # We cancel moves that are too short to avoid useless processing and then keep fluidity
        """if -0.001 < self._vel_x < 0.001:
            self._vel_x = 0
        if -0.001 < self._vel_y < 0.001:
            self._vel_y = 0

        hitbox_copy = self.get_hitbox().copy()
        hitbox_copy.expand(self._vel_x, self._vel_y)

        entities = self.get_stage().entities

        i = 0
        while i < len(entities) and self._vel_x != 0:
            self._vel_x = self._hitbox.calc_offset_x(entities[i].get_hitbox(), self._vel_x)
            i += 1

        i = 0
        while i < len(entities) and self._vel_y != 0:
            self._vel_y = self._hitbox.calc_offset_x(entities[i].get_hitbox(), self._vel_y)
            i += 1
        """

        self._cached_hitbox.set_from(self._hitbox)
        self._cached_hitbox.expand(dx, dy)

        self._cached_hitboxes.clear()

        for entity in self._stage.foreach_colliding_entity(self._cached_hitbox, predicate=self._has_entity_hard_box):
            self._cached_hitboxes.append(entity._hitbox)

        if dx != 0:
            for box in self._cached_hitboxes:
                dx = box.calc_offset_x(self._hitbox, dx)
            self._hitbox.move(dx, 0)

        if dy != 0:
            for box in self._cached_hitboxes:
                dy = box.calc_offset_y(self._hitbox, dy)
            self._hitbox.move(0, dy)

        self._cached_hitboxes.clear()

        if dx != 0 and abs(dx) < 0.01:
            dx = 0

        if dy != 0 and abs(dy) < 0.01:
            dy = 0

        self._vel_x = dx
        self._vel_y = dy

        self._reset_pos_to_box()
