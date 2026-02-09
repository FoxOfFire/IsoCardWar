from enum import Enum, auto

import esper
import pygame

from common import SETTINGS_REF, BoundingBox
from layer2.tags import UIElementComponent

from .rendering_asset_loader import get_font


class RenderLayerEnum(Enum):
    CARD = auto()
    ISO = auto()


def bb_to_rect(bb: BoundingBox) -> pygame.Rect:
    return pygame.Rect(bb.left, bb.top, bb.width, bb.height)


def sort_by_bb(ent: int, side: int) -> float:
    assert esper.entity_exists(ent)

    """
    0-left 1-right 2-top 3-bottom
    """
    return esper.component_for_entity(ent, BoundingBox).points[side]


def draw_text_on_surf(screen: pygame.Surface, ent: int) -> None:
    assert esper.entity_exists(ent)

    ui_elem = esper.try_component(ent, UIElementComponent)
    assert ui_elem is not None

    for text in ui_elem.text:
        text_surf = get_font().render(
            text.text(), False, SETTINGS_REF.FONT_COLOR
        )
        screen.blit(text_surf, text_surf.get_rect(center=text.offset))
