from typing import Dict, Optional

import esper
import pygame

from common import SETTINGS_REF
from layer2.tags import UIElementComponent

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF


class FontAssetContainer:
    _FONT: Optional[pygame.font.Font] = None
    _FONT_ASSET_DIR = "fonts"
    _FONT_NAME = "virtupetpixies.ttf"
    _TEXT_SURF_DICT: Dict[str, pygame.Surface] = {}

    def draw_text_on_surf(self, screen: pygame.Surface, ent: int) -> None:
        if self._FONT is None:

            if SETTINGS_REF.LOG_ASSET_LOADING:
                logger.info("loaded font")
            self._FONT = RENDER_ASSET_REF.load_font(
                self._FONT_ASSET_DIR, self._FONT_NAME
            )
        ui_elem = esper.component_for_entity(ent, UIElementComponent)

        for text in ui_elem.text:
            text_surf = self._TEXT_SURF_DICT.get(text.text())

            if text_surf is None:
                text_surf = self._FONT.render(
                    text.text(), False, SETTINGS_REF.FONT_COLOR
                )
                self._TEXT_SURF_DICT.update({text.text(): text_surf})

            screen.blit(text_surf, text_surf.get_rect(center=text.offset))


FONT_ASSET_REF = FontAssetContainer()
