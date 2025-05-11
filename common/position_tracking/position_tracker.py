from functools import partial
from typing import Iterable, Tuple

import esper
import rtree

from .bounding_box import BoundingBox

_tracked_by_any_tracker: dict[str, set[int]] = dict()


class TrackingError(Exception):
    """Exception raised, when tracking is misused"""


class PlainError(TrackingError):
    """Exception raised when a plain is misused"""


class OutOfBoundsError(TrackingError):
    """Exception raised, when an entity would be out of bounds"""


# The position tracker class shouldn't know what kind of tags it has to possibly track,
# so something like this should be in core:

# class UITrackerTag(NamedTuple):
#     pass


# class GameTrackerTag(NamedTuple):
#     pass


class PositionTracker(esper.Processor):
    """
    Position Tracker Processor

    This processor is used to update and track the entity positions in the game.
    """

    __tracked_entities: set[int]
    __index: rtree.index.Index
    __plain: int
    __plain_bb: BoundingBox
    __tag_type: type

    def __init__(self, tag_type: type, plain: int) -> None:
        props = rtree.index.Property(
            dimension=2,
            storage=rtree.index.RT_Memory,
        )

        self.__index = rtree.index.Index(properties=props, interleaved=False)
        self.__tracked_entities = set[int]()
        self.__tag_type = tag_type

        if _tracked_by_any_tracker.get(esper.current_world) is None:
            _tracked_by_any_tracker[esper.current_world] = set()

        if plain in _tracked_by_any_tracker[esper.current_world]:
            raise PlainError("Plain is already associated with a tracker")

        _tracked_by_any_tracker[esper.current_world].add(plain)

        esper.add_component(plain, self.__tag_type())
        self.__plain_bb = esper.component_for_entity(plain, BoundingBox)
        self.__tracked_entities.add(plain)
        self.__plain = plain
        self.__index.insert(plain, self.__plain_bb.points)

    @property
    def plain(self) -> int:
        return self.__plain

    def is_inbounds(self, bounding_box: BoundingBox) -> bool:
        map_left, map_right, map_top, map_bottom = self.__plain_bb.points
        return (
            bounding_box.left >= map_left
            and bounding_box.right <= map_right
            and bounding_box.top >= map_top
            and bounding_box.bottom <= map_bottom
        )

    def process(self) -> None:
        """
        Adds newly tagged entities,
        removes dead entities from tracker, always call this after entities are killed,
        does not support espert.delete_entity(..., immediate=True)
        updates entity bounding boxes in index
        """
        for entity, (b_box, _) in esper.get_components(BoundingBox, self.__tag_type):
            if not esper.entity_exists(entity):
                continue

            if entity not in self.__tracked_entities:
                if entity in _tracked_by_any_tracker[esper.current_world]:
                    raise TrackingError(f"{entity} is already tracked by a tracker")

                if not self.is_inbounds(b_box):
                    raise OutOfBoundsError(f"Tried to track {entity} out of bounds.")

                _tracked_by_any_tracker[esper.current_world].add(entity)
                self.__tracked_entities.add(entity)
                self.__index.add(entity, b_box.points)

            if b_box.has_nonzero_delta:
                if entity == self.__plain:
                    raise PlainError(f"Tried to move the plain: {self.__plain}.")

                next_bb = b_box.after_update()

                # Can't remove the code dublication from this without getattr horror
                overhang_left = self.__plain_bb.left - next_bb.left
                if overhang_left > 0:
                    b_box.move_right(overhang_left)
                overhang_right = next_bb.right - self.__plain_bb.right
                if overhang_right > 0:
                    b_box.move_left(overhang_right)

                overhang_top = self.__plain_bb.top - next_bb.top
                if overhang_top > 0:
                    b_box.move_down(overhang_top)
                overhang_bottom = next_bb.bottom - self.__plain_bb.bottom
                if overhang_bottom > 0:
                    b_box.move_up(overhang_bottom)

                self.__index.delete(entity, b_box.points)
                b_box.update()
                self.__index.insert(entity, b_box.points)

    def untrack(self, entity: int) -> None:
        if entity not in self.__tracked_entities:
            return
        bb = esper.component_for_entity(entity, BoundingBox)
        self.__tracked_entities.remove(entity)
        _tracked_by_any_tracker[esper.current_world].discard(entity)
        self.__index.delete(entity, bb.points)

    def is_tracked(self, entity: int) -> bool:
        return entity in self.__tracked_entities

    def __circle_intersect_cull_bb(
        self, circle: tuple[tuple[float, float], float]
    ) -> BoundingBox:
        (x, y), r = circle
        return BoundingBox(
            left=x - r,
            right=x + r,
            top=y - r,
            bottom=y + r,
        )

    @staticmethod
    def __entity_in_circle(ent: int, circle: tuple[tuple[float, float], float]) -> bool:
        (x, y), r = circle
        bb = esper.component_for_entity(ent, BoundingBox)
        x_distance = abs(x - bb.center[0])
        y_distance = abs(y - bb.center[1])
        # This is faster than taking sqrt on both sides of equation
        return x_distance**2 + y_distance**2 <= r**2

    def intersect(self, bounding_box: BoundingBox) -> list[int]:
        """
        Returns a list of entites that are intersecting with the bounding box
        """
        return list(self.__index.intersection(bounding_box.points))

    def intersect_circle(self, circle: tuple[tuple[float, float], float]) -> list[int]:
        """
        Returns the entity ONLY if the middle of it's bounding box is in the circle

        The circle is represented with a tuple, like: ((x, y), r),
        where (x, y) is the middle or the circle and r is the radius.
        """
        fast_pass_cull_bb = self.__circle_intersect_cull_bb(circle)
        in_circle = partial(self.__entity_in_circle, circle=circle)
        return list(filter(in_circle, self.intersect(fast_pass_cull_bb)))

    def bulk_intersect(
        self, bounding_boxes: Iterable[BoundingBox]
    ) -> Tuple[list[int], list[int]]:
        """
        Returns a list of entity entities
        that intersecting any of the given bounding boxes,
        paired whith how many bounding boxes the given entity is intersecting
        """
        hits = dict[int, int]()
        for bb in bounding_boxes:
            current_hits = self.intersect(bb)
            for ent in current_hits:
                hits[ent] = hits.get(ent, 0) + 1

        return list(hits.keys()), list(hits.values())

    def bulk_intersect_circles(
        self, middle: tuple[float, float], radiuses: Iterable[float]
    ) -> tuple[list[int], list[int]]:
        fast_pass_cull_bb = self.__circle_intersect_cull_bb((middle, max(radiuses)))
        culled_entites = self.intersect(fast_pass_cull_bb)

        hits = dict[int, int]()
        for r in radiuses:
            in_circle = partial(self.__entity_in_circle, circle=(middle, r))
            for ent in filter(in_circle, culled_entites):
                hits[ent] = hits.get(ent, 0) + 1

        return list(hits.keys()), list(hits.values())
