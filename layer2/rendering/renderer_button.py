from typing import Optional, Tuple, Type

import esper
import pygame

from common import POS_PROC_REF, SETTINGS_REF, BoundingBox
from layer2.tags import UIElementComponent

from .asset_container_ui import UI_ASSET_REF
from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import UIElemSprite, UIElemType


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

    def _check_visible(
        self, ent: int
    ) -> Optional[Tuple[UIElemSprite, UIElementComponent]]:
        ui_sprite = esper.try_component(ent, UIElemSprite)
        if ui_sprite is None:
            return None

        ui_elem = esper.try_component(ent, UIElementComponent)
        if ui_elem is None:
            return None

        elem_check: Optional[UIElementComponent] = ui_elem
        visible = True
        while elem_check is not None and visible:
            visible = elem_check.is_visible
            if elem_check.parent_elem is None:
                break
            parent = elem_check.parent_elem
            assert isinstance(parent, UIElementComponent)
            elem_check = parent

        if not visible:
            return None
        return ui_sprite, ui_elem

    def draw(self, screen: pygame.Surface) -> None:
        assert self.bb is not None
        for ent in POS_PROC_REF().intersect(self.bb, self.track_tag):
            if not esper.entity_exists(ent):
                continue

            bb = esper.component_for_entity(ent, BoundingBox)
            result = self._check_visible(ent)
            if result is None:
                continue
            ui_sprite, ui_elem = result
            ui_sprite.button_data = ui_elem.button_val
            surf = UI_ASSET_REF.get_button_surf(ui_sprite)[
                ui_elem.state.value - 1
            ].copy()
            if ui_sprite.elem_type == UIElemType.SLIDER:
                t_size = SETTINGS_REF.BUTTON_TILE_SIZE
                w, h = ui_sprite.size
                t = ui_sprite.button_data
                assert w == 1 or h == 1
                assert isinstance(t, float), t
                if w == 1:
                    center = (
                        t_size / 2,
                        (h - 1) * t_size * t + t_size / 2,
                    )
                if h == 1:
                    center = (
                        (w - 1) * t_size * t + t_size / 2,
                        t_size / 2,
                    )

                com = UIElemSprite(UIElemType.SLIDER, (1, 1))
                dot_surf = UI_ASSET_REF.get_button_surf(com)[
                    ui_elem.state.value - 1
                ]
                surf.blit(dot_surf, dot_surf.get_rect(center=center))
            else:
                RENDER_ASSET_REF.draw_text_on_surf(surf, ent)
            screen.blit(surf, surf.get_rect(center=bb.center))
