from entity import MotionEntity
import stage


class Floor(MotionEntity):
    def __init__(self, entity_stage: 'stage.Stage') -> None:
        MotionEntity.__init__(self, entity_stage)

    def update(self) -> None:
        pass

    @staticmethod
    def get_hard_hitbox() -> bool:
        return True
