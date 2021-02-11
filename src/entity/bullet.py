from entity import MotionEntity
import stage


class Bullet(MotionEntity):

    def __init__(self, entity_stage: 'stage.Stage'):
        super().__init__(entity_stage)

    def update(self):
        super().update()
