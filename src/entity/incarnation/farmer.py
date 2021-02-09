from entity.incarnation import Incarnation


class Farmer(Incarnation):
    """
    Implementation of the incarnation Farmer, the classic incarnation. Inherits from incarnation
    """

    def __init__(self) -> None:
        Incarnation.__init__(self)
        self.set_duration(9999.9)

    # GETTER
    @staticmethod
    def get_name() -> str:
        return "farmer"

    def add_to_duration(self, number: float) -> None:
        """
        since the time in farmer is infinite, it's useless to change it
        """
        var = None
