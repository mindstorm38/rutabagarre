from entity.motion_entity.incarnation import Incarnation


class Corn(Incarnation):
    """
    Implementation of the incarnation Corn, the solid attacker. Inherits from incarnation
    """
    def __init__(self):
        Incarnation.__init__(self)

    # GETTER
    @staticmethod
    def get_name() -> str:
        return "corn"

    @staticmethod
    def get_attack() -> float:
        return 1.5

    @staticmethod
    def get_defense() -> float:
        return 0.5

    @staticmethod
    def get_speed_multiplier() -> float:
        return 1.2
