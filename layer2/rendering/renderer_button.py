from dataclasses import dataclass
from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer2 import UIElementComponent

from .log import logger
from .rendering_asset_loader import BUTTON_SURFS, UIElemType
from .utils import draw_text_on_surf


@dataclass
class UIElemSprite:
    elem_type: UIElemType


class ButtonRenderer:
    def __init__(self, pos_track: PositionTracker, tag: Type) -> None:
        super().__init__()
        self.pos_track = pos_track
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )
        logger.info("button render init finished")

    def draw(self, screen: pygame.Surface) -> None:
        for ent in self.pos_track.intersect(self.bb):
            bb = esper.component_for_entity(ent, BoundingBox)
            ui_sprite = esper.try_component(ent, UIElemSprite)
            ui_elem = esper.try_component(ent, UIElementComponent)
            if ui_sprite is None or ui_elem is None:
                continue
            surf = BUTTON_SURFS[ui_sprite.elem_type][ui_elem.state.value - 1].copy()
            draw_text_on_surf(surf, ent)

            screen.blit(surf, surf.get_rect(center=bb.center))
