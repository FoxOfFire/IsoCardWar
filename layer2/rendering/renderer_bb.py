from functools import partial
from typing import Type

import esper
import pygame

from common import POS_PROC_REF, SETTINGS_REF, BoundingBox

from .log import logger
from .utils import bb_to_rect, sort_by_bb


class BBRenderer:
    def __init__(self, cam_tag: Type, track_tag: Type) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )
        logger.info("bb render init finished")

    def draw(self, screen: pygame.Surface) -> None:
        if not SETTINGS_REF.RENDER_BBS:
            return

        ent_list = sorted(
            POS_PROC_REF.intersect(self.bb, self.track_tag),
            key=partial(sort_by_bb, side=3),
        )

        for ent in ent_list:
            assert esper.entity_exists(ent)

            bb = esper.component_for_entity(ent, BoundingBox)

            surf = pygame.Surface((bb.width, bb.height), flags=pygame.SRCALPHA)
            surf.fill(pygame.Color(40, 60, 20, 50))

            screen.blit(surf, bb_to_rect(bb))
