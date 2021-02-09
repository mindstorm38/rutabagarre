from entity.incarnation import Incarnation


class Potato(Incarnation):
    """
    Implementation of the incarnation Potato, the solid attacker. Inherits from incarnation
    """
    def __init__(self):
        Incarnation.__init__(self)

    # GETTER
    @staticmethod
    def get_name() -> str:
        return "potato"

    @staticmethod
    def get_attack() -> float:
        return 1.5

    @staticmethod
    def get_defense() -> float:
        return 1.5

    @staticmethod
    def get_speed_multiplier() -> float:
        return 0.7
