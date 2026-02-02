from typing import Dict, List, Type

import esper

from common.position_tracking.bb_rtree import BBRTree
from common.position_tracking.bounding_box import BoundingBox
from common.position_tracking.tags import Moved, Removed, TrackBase, Untracked


class PositionProcessor(esper.Processor):
    __tracked_types: Dict[Type, BBRTree] = {}

    def __init__(self, tracked_types: List[Type]) -> None:
        super().__init__()
        for t in tracked_types:
            self.__tracked_types.update({t: BBRTree(t)})

    def process(self) -> None:
        for ent, _ in esper.get_component(Moved):
            esper.remove_component(ent, Moved)
            for tag in esper.components_for_entity(ent):
                if isinstance(tag, TrackBase):
                    self.__tracked_types[type(tag)].update(ent)

        for ent, _ in esper.get_component(Untracked):
            esper.remove_component(ent, Untracked)
            for tag in esper.components_for_entity(ent):
                if isinstance(tag, TrackBase):
                    self.__tracked_types[type(tag)].insert(ent)
                    break

        for ent, _ in esper.get_component(Removed):
            esper.remove_component(ent, Removed)
            for tag in esper.components_for_entity(ent):
                if isinstance(tag, TrackBase):
                    self.__tracked_types[type(tag)].delete_current(ent)
                    break

    def intersect(self, bb: BoundingBox, tag: Type) -> List[int]:
        return self.__tracked_types[tag].intersect(bb)

    def intersect_ent_type(self, bb: BoundingBox, ent: int) -> List[int]:
        tag: Type
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, TrackBase):
                tag = type(comp)
        return self.intersect(bb, tag)

    def intersect_ent(self, ent: int) -> List[int]:
        bb: BoundingBox
        tag: Type
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, TrackBase):
                tag = type(comp)
            if isinstance(comp, BoundingBox):
                bb = comp
        return self.intersect(bb, tag)
