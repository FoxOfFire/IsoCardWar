from typing import Tuple


class BoundingBox:
    left: float = 0
    right: float = 0
    top: float = 0
    bottom: float = 0

    prev_left: float = 0
    prev_right: float = 0
    prev_top: float = 0
    prev_bottom: float = 0

    _vel_x: float = 0
    _vel_y: float = 0

    def __init__(
        self, left: float, right: float, top: float, bottom: float
    ) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top

    @property
    def points(self) -> tuple[float, float, float, float]:
        return (self.left, self.right, self.top, self.bottom)

    @property
    def prev_points(self) -> Tuple[float, float, float, float]:
        return (
            self.prev_left,
            self.prev_right,
            self.prev_top,
            self.prev_bottom,
        )

    @property
    def has_nonzero_velocity(self) -> bool:
        return self._vel_x != 0 or self._vel_y != 0

    def set_velocity(self, vel_x: float, vel_y: float) -> None:
        self._vel_x = vel_x
        self._vel_y = vel_y

    def add_velocity(self, vel_x: float, vel_y: float) -> None:
        self._vel_x += vel_x
        self._vel_y += vel_y

    def move_towards_point(self, point: tuple[float, float], by: float) -> None:
        def lerp(a: float, b: float, t: float) -> float:
            return t * a + (1 - t) * b

        self._vel_x += lerp(self.center[0], point[0], by)
        self._vel_y += lerp(self.center[1], point[1], by)
