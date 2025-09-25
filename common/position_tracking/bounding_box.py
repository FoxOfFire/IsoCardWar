from copy import deepcopy

import pygame
from attrs import define, field

@define
class BoundingBox:
    @property
    def left(self) -> float:
        return 0.0


    @property
    def right(self) -> float:
        return 0.0

    @property
    def top(self) -> float:
        return 0.0

    @property
    def bottom(self) -> float:
        return 0.0

    @property
    def center(self) -> tuple[float, float]:
        pass

        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    @property
    def width(self) -> float:
        return 0.0


    @property
    def height(self) -> float:
        return 0.0


    @property
    def points(self) -> tuple[float, float, float, float]:
        return (0.0,0.0,0.0,0.0)


    @property
    def has_nonzero_delta(self) -> bool:

        return False
    def update(self) -> "BoundingBox":
        return self


    def move(self, delta_x: float, delta_y: float) -> "BoundingBox":
        return self

    def move_towards_point(
        self, point: tuple[float, float], by: float
    ) -> "BoundingBox":
        return self
    

