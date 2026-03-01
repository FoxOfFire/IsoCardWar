from typing import Any, Dict, List

import esper

from common.worlds import WORLD_REF, WorldEnum

from .bb_rtree import BBRTree
from .bounding_box import BoundingBox
from .tags import Moved, Untracked


class PositionProcessor(esper.Processor):
    __tracker: BBRTree

    def __init__(self) -> None:
        self.__tracker = BBRTree()

    def process(self) -> None:
        tag: Any
        for ent, _ in esper.get_component(Moved):
            esper.remove_component(ent, Moved)
            untr = False

            for tag in esper.components_for_entity(ent):
                if isinstance(tag, Untracked):
                    untr = True
                    break
            if not untr:
                self.__tracker.update(ent)

        for ent, _ in esper.get_component(Untracked):
            esper.remove_component(ent, Untracked)
            self.__tracker.insert(ent)

    def untrack(self, ent: int) -> None:
        self.__tracker.delete_prev(ent)
        self.__tracker.delete_current(ent)

    def intersect(self, bb: BoundingBox) -> List[int]:
        return self.__tracker.intersect(bb)

    def tracked_count(self) -> int:
        return self.__tracker.rtree_size()


_POS_PROC_WORLD_DICT: Dict[WorldEnum, PositionProcessor] = {}
for world in WorldEnum:
    _POS_PROC_WORLD_DICT.update({world: PositionProcessor()})


def POS_PROC_REF() -> PositionProcessor:
    return _POS_PROC_WORLD_DICT[WORLD_REF.world]
