from abc import ABC, abstractmethod
from entity.hitbox import Hitbox
import stage


class Entity(ABC):

    UID_COUNTER = 0

    def __init__(self, entity_stage: 'stage.Stage'):

        self._uid = self.new_uid()

        self._stage: 'stage.Stage' = entity_stage
        self._x: float = 0.0
        self._y: float = 0.0
        self._hitbox = Hitbox(0, 0, 0, 0)

    @classmethod
    def new_uid(cls) -> int:
        cls.UID_COUNTER += 1
        return cls.UID_COUNTER

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
        return False

    # SETTERS
    def set_x(self, x: float) -> None:
        # self._x = x
        raise ValueError("deprecated")

    def set_y(self, y: float) -> None:
        # self._y = y
        raise ValueError("deprecated")

    def set_position(self, x: float, y: float):
        self._x = x
        self._y = y
        self._setup_box_pos(x, y)

    def set_stage(self, stage_to_set: 'stage.Stage') -> None:
        # self._stage = stage_to_set
        # Une entité ne change pas de stage
        raise ValueError("deprecated")

    def set_hitbox(self, the_hitbox: Hitbox) -> None:
        # self._hitbox = the_hitbox
        # On ne défini plus la hitbox par le setter
        raise ValueError("deprecated")

    # ADDERS

    def add_to_x(self, number: float) -> None:
        self._x += number

    def add_to_y(self, number: float) -> None:
        self._y += number

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

    # GETTERS

    def get_vel_x(self) -> float:
        return self._vel_x

    def get_vel_y(self) -> float:
        return self._vel_y

    # SETTERS

    def set_vel_x(self, x: float) -> None:
        # self._vel_x = x
        raise ValueError("deprecated")

    def set_vel_y(self, y: float) -> None:
        # self._vel_y = y
        raise ValueError("deprecated")

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
        self.move_position()

    def update_natural_velocity(self) -> None:
        self._vel_x *= MotionEntity.NATURAL_FRICTION
        self._vel_y = self._vel_y * MotionEntity.NATURAL_FRICTION - MotionEntity.NATURAL_GRAVITY

    def move_position(self) -> None:
        """
        Moves the entity and its hitbox following its actual velocity,
        taking care of other hitboxes onto the stage
        """

        # We cancel moves that are too short to avoid useless processing and then keep fluidity
        if -0.001 < self._vel_x < 0.001:
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

        self.get_hitbox().move(self._vel_x, self._vel_y)
        self._reset_pos_to_box()
