from enum import Enum, auto

import esper
import pygame

from common import BoundingBox
from common.constants import FONT_COLOR
from layer2 import UIElementComponent

from .rendering_asset_loader import get_font


class RenderLayerEnum(Enum):
    CARD = auto()
    ISO = auto()


def bb_to_rect(bb: BoundingBox) -> pygame.Rect:
    return pygame.Rect(bb.left, bb.top, bb.width, bb.height)


def sort_by_bb(ent: int, side: int) -> float:
    """
    0-left 1-right 2-top 3-bottom
    """
    return esper.component_for_entity(ent, BoundingBox).points[side]


def draw_text_on_surf(screen: pygame.Surface, ent: int) -> None:
    ui_elem = esper.try_component(ent, UIElementComponent)
    if ui_elem is None:
        return

    for text in ui_elem.text:
        text_surf = get_font().render(text.text(), False, FONT_COLOR)
        screen.blit(text_surf, text_surf.get_rect(center=text.offset))
