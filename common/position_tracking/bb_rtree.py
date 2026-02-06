from typing import List, Optional, Type

import esper
import rtree

from .bounding_box import BoundingBox


class BBRTree:
    __rt_index: rtree.index.Index
    __tracked_tag: Type
    __tracked_boxes: int = 0

    def __init__(self, tag: Type) -> None:
        rt_props = rtree.index.Property(
            dimension=2,
            storage=rtree.index.RT_Memory,
        )
        self.__rt_index = rtree.index.Index(
            properties=rt_props, interleaved=False
        )
        self.tracked_tag = tag

    def insert(self, ent: int) -> None:
        bb = esper.component_for_entity(ent, BoundingBox)
        self.__rt_index.insert(ent, bb.points)
        self.__tracked_boxes += 1

    def delete_current(self, ent: int) -> None:
        bb = esper.component_for_entity(ent, BoundingBox)
        self.__rt_index.delete(ent, bb.points)

    def delete_prev(self, ent: int) -> None:
        bb = esper.component_for_entity(ent, BoundingBox)
        self.__rt_index.delete(ent, bb.prev_points)
        self.__tracked_boxes -= 1

    def update(self, ent: int) -> None:
        bb = esper.component_for_entity(ent, BoundingBox)
        self.delete_prev(ent)
        self.insert(ent)

    def intersect(self, bb: BoundingBox) -> List[int]:
        return list(self.__rt_index.intersection(bb.points))

    def rtree_size(self) -> int:
        return self.__tracked_boxes
