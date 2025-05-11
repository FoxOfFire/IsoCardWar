from copy import deepcopy

import pygame
from attrs import define, field


@define
class BoundingBox:
    """
    # Bounding Box component

    This component is used to track the absolute position of an entity on the map.

    The origin point (0, 0) is the top-left side of the map.

    All attributes should be positive.

    Attributes:
        left: The left side of the entity from origin, smaller than `right`
        right: The right side of the entity from origin, larger than `left`
        top: The top side of the entity from origin, smaller than `bottom`
        bottom: The bottom side of the entity from origin, larger than `top`
    """

    # We start the private fields with `_` instead of `__`,
    # because that's what attrs supports

    _left: float = field(default=0)
    _right: float = field(default=0)
    _top: float = field(default=0)
    _bottom: float = field(default=0)

    delta_left: float = field(default=0, init=False)
    delta_right: float = field(default=0, init=False)
    delta_top: float = field(default=0, init=False)
    delta_bottom: float = field(default=0, init=False)

    # We have to write getters by hand,
    # because they aren't generated automatically if they are private
    @property
    def left(self) -> float:
        return self._left

    @property
    def right(self) -> float:
        return self._right

    @property
    def top(self) -> float:
        return self._top

    @property
    def bottom(self) -> float:
        return self._bottom

    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    @property
    def width(self) -> float:
        return self._right - self._left

    @property
    def height(self) -> float:
        return self._bottom - self._top

    @property
    def points(self) -> tuple[float, float, float, float]:
        return (self.left, self.right, self.top, self.bottom)

    @property
    def has_nonzero_delta(self) -> bool:
        return (
            self.delta_left != 0
            or self.delta_right != 0
            or self.delta_top != 0
            or self.delta_bottom != 0
        )

    def update(self) -> "BoundingBox":
        """
        Updates `left`, `right`, `top`, `bottom` according to their respective deltas.
        Should only be called by PositionTracker.
        """
        self._left += self.delta_left
        self._right += self.delta_right
        self._top += self.delta_top
        self._bottom += self.delta_bottom

        self.delta_left = 0
        self.delta_right = 0
        self.delta_top = 0
        self.delta_bottom = 0

        return self

    def after_update(self) -> "BoundingBox":
        self_copy = deepcopy(self)
        return self_copy.update()

    def move_up(self, by: float) -> "BoundingBox":
        self.delta_top += -by
        self.delta_bottom += -by
        return self

    def move_down(self, by: float) -> "BoundingBox":
        self.delta_top += by
        self.delta_bottom += by
        return self

    def move_left(self, by: float) -> "BoundingBox":
        self.delta_left += -by
        self.delta_right += -by
        return self

    def move_right(self, by: float) -> "BoundingBox":
        self.delta_left += by
        self.delta_right += by
        return self

    def move_towards(self, point: tuple[float, float], by: float) -> "BoundingBox":
        point_vec = pygame.math.Vector2(point)
        left_top_vec = pygame.math.Vector2(self.center)
        direction = point_vec - left_top_vec
        distance = direction.length()

        if distance == 0 or distance < by:
            movement = point_vec - left_top_vec
        else:
            direction.scale_to_length(by)
            movement = direction

        self.delta_left += movement.x
        self.delta_right += movement.x
        self.delta_top += movement.y
        self.delta_bottom += movement.y

        return self

    def is_intersecting_line_segment(
        self, point1: tuple[float, float], point2: tuple[float, float]
    ) -> bool:
        """
        Determines whether a line segment intersects the bounding box.

        This method checks if the line segment defined by `point1` and `point2`
        intersects any of the four edges of the bounding box. A line segment is
        considered to be intersecting, if one of the points is in the bounding box
        or if the line intersects an edge of the bounding box.

        Parameters:
            point1 (tuple[float, float]): The first endpoint of the line segment.
            point2 (tuple[float, float]): The second endpoint of the line segment.
        """
        # The algorithm for intersecting with a bounding box is the following:

        # We will get the four line segments for the 4 bounding box edges
        # If the line segment intersects any of them,
        # we know the line intersects the bounding box.

        # To find if 2 line segments intersect we will find the point
        # where they would intersect if they were infinite lines
        # we will use the following algo:
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

        for x, y in [point1, point2]:
            # This also returns True if the line is coincidence
            if self.left <= x <= self.right and self.top <= y <= self.bottom:
                return True  # one of the points is in the BoundingBox

        EPSILON = 1e-12

        def intersection_point(
            line1: tuple[tuple[float, float], tuple[float, float]],
            line2: tuple[tuple[float, float], tuple[float, float]],
        ) -> tuple[float, float] | None:
            (x1, y1), (x2, y2) = line1
            (x3, y3), (x4, y4) = line2

            denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denominator) < EPSILON:
                return None

            factor1 = x1 * y2 - y1 * x2
            factor2 = x3 * y4 - y3 * x4

            p_x = (factor1 * (x3 - x4) - factor2 * (x1 - x2)) / denominator
            p_y = (factor1 * (y3 - y4) - factor2 * (y1 - y2)) / denominator

            return p_x, p_y

        # Not checking for collinearity, intersection_point already ensures that
        def collinear_point_on_line_segment(
            point: tuple[float, float],
            segment: tuple[tuple[float, float], tuple[float, float]],
        ) -> bool:
            p_x, p_y = point
            (x1, y1), (x2, y2) = segment
            return (
                min(x1, x2) - EPSILON <= p_x <= max(x1, x2) + EPSILON
                and min(y1, y2) - EPSILON <= p_y <= max(y1, y2) + EPSILON
            )

        line_segment = (point1, point2)
        bounding_box_edges = [
            ((self.left, self.top), (self.right, self.top)),
            ((self.left, self.bottom), (self.right, self.bottom)),
            ((self.left, self.top), (self.left, self.bottom)),
            ((self.right, self.top), (self.right, self.bottom)),
        ]

        for edge in bounding_box_edges:
            point = intersection_point(line_segment, edge)
            if point is None:
                continue

            on_segment = collinear_point_on_line_segment(point, line_segment)
            on_edge = collinear_point_on_line_segment(point, edge)

            if on_segment and on_edge:
                return True

        return False
