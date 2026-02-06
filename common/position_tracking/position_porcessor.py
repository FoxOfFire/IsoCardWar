from typing import Any, Dict, List, Type

import esper

from .bb_rtree import BBRTree
from .bounding_box import BoundingBox
from .tags import Moved, TrackBase, Untracked


class PositionProcessor(esper.Processor):
    __tracker_dict: Dict[Type, BBRTree] = {}
    __tracked_tags: List[Type] = []

    def __init__(self) -> None:
        super().__init__()

    def process(self) -> None:
        tag: Any
        for ent, _ in esper.get_component(Moved):
            esper.remove_component(ent, Moved)
            ty = None
            for tag in esper.components_for_entity(ent):
                if isinstance(tag, TrackBase):
                    ty = tag
                if isinstance(tag, Untracked):
                    ty = None
                    break

            if ty is not None:
                self.__tracker_dict[type(ty)].update(ent)

        for ent, _ in esper.get_component(Untracked):
            esper.remove_component(ent, Untracked)
            for tag in esper.components_for_entity(ent):
                if isinstance(tag, TrackBase):
                    self.__tracker_dict[type(tag)].insert(ent)
                    break

    def untrack(self, ent: int) -> None:
        comp: Any
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, TrackBase):
                tag = type(comp)
            if isinstance(comp, BoundingBox):
                bb = comp
        self.__tracker_dict[tag].delete_prev(ent)
        self.__tracker_dict[tag].delete_current(ent)

    def intersect(self, bb: BoundingBox, tag: Type) -> List[int]:
        return self.__tracker_dict[tag].intersect(bb)

    def intersect_ent_type(self, bb: BoundingBox, ent: int) -> List[int]:
        comp: Any
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, TrackBase):
                tag = type(comp)
        return self.intersect(bb, tag)

    def intersect_ent(self, ent: int) -> List[int]:
        comp: Any
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, TrackBase):
                tag = type(comp)
            if isinstance(comp, BoundingBox):
                bb = comp
        return self.intersect(bb, tag)

    def tracked_count_of_type(self, ty: Type) -> int:
        assert ty in self.__tracked_tags
        return self.__tracker_dict[ty].rtree_size()

    def start_tracking_type(self, ty: Type) -> None:
        self.__tracked_tags.append(ty)
        self.__tracker_dict.update({ty: BBRTree(ty)})


POS_PROC_REF = PositionProcessor()
