from entity.player import Player, IncarnationType
from entity import MotionEntity
from typing import cast
import stage


class Item(MotionEntity):

    def __init__(self, entity_stage: 'stage.Stage', incarnation_type: IncarnationType) -> None:
        super().__init__(entity_stage)
        self._incarnation_type = incarnation_type

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x - 0.2, y, x + 0.2, y + 0.4)

    def get_incarnation_type(self) -> IncarnationType:
        return self._incarnation_type

    def update(self) -> None:

        super().update()

        for target_player in self._stage.foreach_colliding_entity(self._hitbox, predicate=Player.is_player):
            if cast(Player, target_player).load_incarnation(self._incarnation_type):
                self.set_dead()
                break
