from typing import Dict, List, Tuple, Type
import esper

from common.position_tracking.bb_rtree import BBRTree
from common.position_tracking.bounding_box import BoundingBox
from common.position_tracking.tags import Moved, Untracked


class PositionProcessor(esper.Processor):
    __tracked_types: Dict[Type,Tuple[BBRTree,List[int]]] = {}
    def __init__(self,tracked_types: List[Type]) -> None:
        super().__init__()
        for t in tracked_types:
            self.__tracked_types.update({t:(BBRTree(t),[])})

    
    def process(self) -> None:
        for tree,ents in self.__tracked_types.values():
            for ent in ents:
                if esper.has_component(ent,Moved):
                    tree.update(ent)
                    esper.remove_component(ent,Moved)
        for ent ,(bb, _) in esper.get_components(BoundingBox,Untracked):
            for t in self.__tracked_types.keys():
                if esper.has_component(ent,t):
                    tree, ents = self.__tracked_types[t]
                    tree.insert(ent,bb)
                    esper.remove_component(ent,Untracked)
                    break
            assert not esper.has_component(ent,Untracked)
