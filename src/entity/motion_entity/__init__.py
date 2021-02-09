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
        # TODO : intégrer la gestion des hitbox
        self.add_to_x(
            self.get_vel_x()
        )
        self.add_to_y(
            self.get_vel_y()
        )

