from __future__ import annotations


class Hitbox:
    """
    Class that defines a rectangular hitbox with absolute position
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
    def copy(self) -> Hitbox:
        return Hitbox(self._x_tl, self._y_tl, self._x_ur, self._y_ur)

    def move(self, x: float, y: float) -> None:
        """
        Moves the hitbox following the vector (x,y)
        """
        self._x_tl += x
        self._x_ur += x
        self._y_tl += y
        self._y_ur += y

    def expand(self, x: float, y: float) -> None:
        """
        If x > 0 it expands x from the right-bottom angle.
        If y > 0 it expands y from the left-upper angle.
        """
        if x > 0.0:
            self._x_ur += x
        else:
            self._x_tl += x

        if y > 0.0:
            self._y_tl += y
        else:
            self._y_tl += y

    def intersects_x(self, other_hitbox: Hitbox) -> bool:
        """
        :return: if other_hitbox intersects with this one
        """
        return not (
            other_hitbox._x_tl >= self._x_ur or
            other_hitbox._x_ur <= self._x_tl
        )

    def intersects_y(self, other_hitbox: Hitbox) -> bool:
        """
        :return: if other_hitbox intersects with this one
        """
        return not (
            other_hitbox._y_tl <= self._y_ur or
            other_hitbox._y_ur >= self._y_tl
        )

    def calc_offset_x(self, other_hitbox: Hitbox, x: float) -> float:
        """
        Calculates how far we can move among the x-axis without hitting other_hitbox.
        Supposes that else we we hit other_hitbox
        :return: `x +/- (what is necessary to be able to move)`
        """
        if x > 0:
            # We go left
            return other_hitbox._x_tl - (self.get_x_ur() + x)
        elif x < 0:
            # We go right
            return other_hitbox._x_ur - (self.get_x_ur() + x)
        else:
            raise ValueError("Error: it's abnormal to calculate the offset when x = 0: something goes wrong")

    def calc_offset_y(self, other_hitbox: Hitbox, y: float) -> float:
        """
        Calculates how far we can move among the y-axis without hitting other_hitbox.
        Supposes that else we we hit other_hitbox
        :return: `y +/- (what is necessary to be able to move)`
        """
        if y > 0:
            # We go down
            return other_hitbox._y_tl - (self.get_y_ur() + y)
        elif y < 0:
            # We go up
            return other_hitbox._y_ur - (self.get_y_tl() + y)
        else:
            raise ValueError("Error: it's abnormal to calculate the offset when y = 0: something goes wrong")
