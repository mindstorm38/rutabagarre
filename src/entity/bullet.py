from entity import MotionEntity, Entity
from entity import player
import stage


class Bullet(MotionEntity):

    NATURAL_GRAVITY = 0
    GROUND_FRICTION = 1
    AIR_FRICTION = 1

    def __init__(self, entity_stage: 'stage.Stage', owner: 'player.Player', damage: float, dx: float):
        super().__init__(entity_stage)
        self._owner = owner
        self._damage = damage
        self.set_velocity(dx, 0)

    def update(self):
        super().update()
        if abs(self._vel_x) < 0.1 or self._x < -1 or self._x > self._stage.get_size()[0] + 1:
            self.set_dead()

    def _entity_bound_box_predicate(self, entity: Entity) -> bool:
        return super()._entity_bound_box_predicate(entity) or (
                isinstance(entity, player.Player) and entity != self._owner and not self._owner.is_sleeping()
        )

    def _entity_bound_box_post_predicate(self, entity: Entity) -> bool:
        if isinstance(entity, player.Player):
            if not entity.is_invincible():
                self._owner.remove_hp_to_other(entity, self._damage)
                entity.push_animation("hit")
            self.set_dead()
            return False
        return True

    def _setup_box_pos(self, x: float, y: float):
        self._hitbox.set_positions(x - 0.1, y - 0.1, x + 0.1, y + 0.1)

    def _reset_pos_to_box(self):
        self._x = self._hitbox.get_mid_x()
        self._y = self._hitbox.get_mid_y()
