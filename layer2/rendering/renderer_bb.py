from functools import partial
from typing import Optional, Type

import esper
import pygame

from common import COLOR_REF, POS_PROC_REF, SETTINGS_REF, BoundingBox

from .utils import bb_to_rect, sort_by_bb


class BBRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self) -> None:
        super().__init__()
        self.bb = None

    def draw(self, screen: pygame.Surface) -> None:
        if not SETTINGS_REF.RENDER_BBS:
            return
        assert self.bb is not None

        ent_list = sorted(
            POS_PROC_REF().intersect(self.bb),
            key=partial(sort_by_bb, side=3),
        )

        col = pygame.Color(COLOR_REF.SWAMP)
        col.a = 50
        for ent in ent_list:
            assert esper.entity_exists(ent)

            bb = esper.component_for_entity(ent, BoundingBox)

            surf = pygame.Surface((bb.width, bb.height), flags=pygame.SRCALPHA)

            surf.fill(col)

            screen.blit(surf, bb_to_rect(bb))
