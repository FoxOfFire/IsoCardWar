from typing import Dict

import esper

from common.worlds import WORLD_REF, WorldEnum

from .bounding_box import BoundingBox
from .tags import Moved


class BBMoveProcessor(esper.Processor):
    def process(self) -> None:
        for ent, bb in esper.get_component(BoundingBox):
            if bb.has_nonzero_velocity:
                bb.prev_right = bb.right
                bb.prev_left = bb.left
                bb.prev_top = bb.top
                bb.prev_bottom = bb.bottom

                bb.right += bb._vel_x
                bb.left += bb._vel_x
                bb.top += bb._vel_y
                bb.bottom += bb._vel_y
                esper.add_component(ent, Moved())


_BB_MOVE_PROC_WORLD_DICT: Dict[WorldEnum, BBMoveProcessor] = {}
for world in WorldEnum:
    _BB_MOVE_PROC_WORLD_DICT.update({world: BBMoveProcessor()})


def BB_MOVE_PROC_REF() -> BBMoveProcessor:
    return _BB_MOVE_PROC_WORLD_DICT[WORLD_REF.world]
