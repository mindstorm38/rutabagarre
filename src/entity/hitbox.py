class HitBox:
    """
    Class that defines a hitbox on absolute position
    """
    def __init__(self, x_tl: float, y_tl: float, x_ur: float, y_ur: float) -> None:
        self._x_tl: float = x_tl
        self._y_tl: float = y_tl
        self._x_ur: float = x_ur
        self._y_ur: float = y_ur

    # GETTERS
    def get_x_tl(self) -> float:
        return self._x_tl

    def get_y_tl(self) -> float:
        return self._y_tl

    def get_x_ur(self) -> float:
        return self._x_ur

    def get_y_ur(self) -> float:
        return self._y_ur

    def get_width(self) -> float:
        return self._x_ur - self._x_tl

    def get_height(self) -> float:
        return self._y_ur - self._y_tl

    # SETTERS
    def set_x_tl(self, x_tl: float) -> None:
        self._x_tl = x_tl

    def set_y_tl(self, y_tl: float) -> None:
        self._y_tl = y_tl

    def set_x_ur(self, x_ur: float) -> None:
        self._x_ur = x_ur

    def set_y_ur(self, y_ur: float) -> None:
        self._y_ur = y_ur

    # OTHER METHODS
    def move(self, x: float, y: float):
        self._x_tl += x
        self._x_ur += x
        self._y_tl += y
        self._y_ur += y
