from typing import List, Optional, Type
import esper
import rtree

from common.position_tracking.bounding_box import BoundingBox

class BBRTree:
    __rt_index: rtree.index.Index
    tracked_tag: Type

    def __init__(self, tag: Type) -> None:
        rt_props = rtree.index.Property(
            dimension=2,
            storage=rtree.index.RT_Memory,
        )
        self.__rt_index = rtree.index.Index(properties=rt_props, interleaved=False)
        self.tracked_tag = tag
 
    def insert(self,ent: int,bb:Optional[BoundingBox] = None)-> None:
        if bb is None:
            bb = esper.component_for_entity(ent,BoundingBox)
        self.__rt_index.insert(ent,bb.points)

    def delete(self,ent:int,bb:Optional[BoundingBox] = None)->None:
        if bb is None:
            bb = esper.component_for_entity(ent,BoundingBox)
        self.__rt_index.delete(ent,bb.prev_points)

    def update(self,ent:int)->None:
        bb = esper.component_for_entity(ent,BoundingBox)
        self.delete(ent,bb)
        self.insert(ent,bb)

    def intersect(self,bb:BoundingBox)->List[int]:
        return list(self.__rt_index.intersection(bb.points))
