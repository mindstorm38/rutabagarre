from entity import Entity
from enum import Enum, auto
import stage
import time


class EffectType(Enum):
    SMOKE = auto()
    SMALL_GROUND_DUST = auto()
    BIG_GROUND_DUST = auto()
    SLEEPING = auto()


class Effect(Entity):

    def __init__(self, entity_stage: 'stage.Stage', effect_type: EffectType, duration: float):
        super().__init__(entity_stage)
        self._effect_type = effect_type
        self._live_until = 0 if duration == 0 else time.monotonic() + duration

    def update(self):
        if self._live_until != 0 and time.monotonic() >= self._live_until:
            self.set_dead()

    def get_effect_type(self) -> EffectType:
        return self._effect_type

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x - 0.05, y, x + 0.05, y + 0.1)

