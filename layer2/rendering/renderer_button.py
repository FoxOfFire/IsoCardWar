from typing import Optional, Type

import esper
import pygame

from common import POS_PROC_REF, BoundingBox
from layer2.tags import UIElementComponent

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import UIElemSprite


class ButtonRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self, track_tag: Type) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = None
        logger.info("button render init finished")

    def draw(self, screen: pygame.Surface) -> None:
        assert self.bb is not None
        for ent in POS_PROC_REF.intersect(self.bb, self.track_tag):
            assert esper.entity_exists(ent)

            bb = esper.component_for_entity(ent, BoundingBox)
            ui_sprite = esper.try_component(ent, UIElemSprite)
            ui_elem = esper.try_component(ent, UIElementComponent)
            if ui_sprite is None or ui_elem is None or not ui_elem.is_visible:
                continue

            surf = RENDER_ASSET_REF.get_button_surf(ui_sprite)[
                ui_elem.state.value - 1
            ].copy()
            RENDER_ASSET_REF.draw_text_on_surf(surf, ent)

            screen.blit(surf, surf.get_rect(center=bb.center))
