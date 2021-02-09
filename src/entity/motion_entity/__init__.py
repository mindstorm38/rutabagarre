from abc import ABC
from src.entity import Entity
import stage


class MotionEntity(Entity, ABC):
    """
    Abstract subclass of Entity that can move
    """
    NATURAL_FRICTION = 0.4

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
        self._vel_y *= MotionEntity.NATURAL_FRICTION

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
