from abc import ABC, abstractmethod
from entity.hitbox import Hitbox
import stage


class Entity(ABC):

    UID_COUNTER = 1

    def __init__(self, entity_stage: 'stage.Stage'):

        self._uid = self.UID_COUNTER
        self.UID_COUNTER += 1

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

    @staticmethod
    def get_hard_hitbox() -> bool:
        return True

    # SETTERS
    def set_x(self, x: float) -> None:
        self._x = x

    def set_y(self, y: float) -> None:
        self._y = y

    def set_stage(self, stage_to_set: 'stage.Stage') -> None:
        self._stage = stage_to_set

    def set_hitbox(self, the_hitbox: Hitbox) -> None:
        self._hitbox = the_hitbox

    # ADDERS
    def add_to_x(self, number: float) -> None:
        self._x += number

    def add_to_y(self, number: float) -> None:
        self._y += number

    @abstractmethod
    def update(self): ...


class MotionEntity(Entity, ABC):
    """
    Abstract subclass of Entity that can move
    """
    NATURAL_FRICTION = 0.4
    NATURAL_GRAVITY = 0.05

    def __init__(self, entity_stage: 'stage.Stage') -> None:
        Entity.__init__(self, entity_stage)
        self._vel_x: float = 0.0
        self._vel_y: float = 0.0

    # GETTERS
    def get_vel_x(self) -> float:
        return self._vel_x

    def get_vel_y(self) -> float:
        return self._vel_y

    # SETTERS
    def set_vel_x(self, x: float) -> None:
        self._vel_x = x

    def set_vel_y(self, y: float) -> None:
        self._vel_y = y

    # OTHER METHODS
    def update(self) -> None:
        self.update_motion()

    def update_motion(self) -> None:
        self.update_natural_velocity()
        self.move_position()

    def update_natural_velocity(self) -> None:
        self._vel_x *= MotionEntity.NATURAL_FRICTION
        self._vel_y = self._vel_y * MotionEntity.NATURAL_FRICTION - MotionEntity.NATURAL_GRAVITY

    def move_position(self) -> None:
        """
        Moves the entity and its hitbox following its actual velocity,
        taking care of other hitboxes onto the stage
        """

        hitbox_copy = self.get_hitbox().copy()
        hitbox_copy.expand(self._vel_x, self._vel_y)

        entities = self.get_stage().entities

        if self._vel_x != 0:
            for entity in entities:
                new_vel_x = self._vel_x
                if entity.get_hard_hitbox() and hitbox_copy.intersects_x(entity.get_hitbox()):
                    new_vel_x = self.get_hitbox().calc_offset_x(entity.get_hitbox(), new_vel_x)
                    if new_vel_x != self._vel_x:
                        self._vel_x = new_vel_x
                        hitbox_copy = self.get_hitbox().copy()
                        hitbox_copy.expand(self._vel_x, self._vel_y)

        if self._vel_y != 0:
            for entity in entities:
                new_vel_y = self._vel_y
                if entity.get_hard_hitbox and hitbox_copy.intersects_y(entity.get_hitbox()):
                    new_vel_y = self.get_hitbox().calc_offset_y(entity.get_hitbox(), new_vel_y)
                    if new_vel_y != self._vel_y:
                        self._vel_y = new_vel_y
                        hitbox_copy = self.get_hitbox().copy()
                        hitbox_copy.expand(self._vel_x, self._vel_y)

        self.get_hitbox().move(self._vel_x, self._vel_y)
        self.add_to_x(self._vel_x)
        self.add_to_y(self._vel_y)
