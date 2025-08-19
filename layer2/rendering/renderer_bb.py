from functools import partial
from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from common.constants import RENDER_BBS

from .log import logger
from .utils import bb_to_rect, sort_by_bb


class BBRenderer:
    def __init__(self, pos_track: PositionTracker, tag: Type) -> None:
        super().__init__()
        self.pos_track = pos_track
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )
        logger.info("bb render init finished")

    def skibidi(self) -> None:
        print("skibidi")


    def draw(self, screen: pygame.Surface) -> None:
        if not RENDER_BBS:
            return

        ent_list = sorted(
            self.pos_track.intersect(self.bb), key=partial(sort_by_bb, side=3)
        )
        plain_bb = esper.component_for_entity(self.pos_track.plain, BoundingBox)

        for ent in ent_list:
            bb = esper.component_for_entity(ent, BoundingBox)
            if bb.points == plain_bb.points:
                continue

            surf = pygame.Surface((bb.width, bb.height), flags=pygame.SRCALPHA)
            surf.fill(pygame.Color(80, 100, 00, 50))
            screen.blit(surf, bb_to_rect(bb))
