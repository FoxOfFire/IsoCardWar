from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional, Tuple

import esper
import pygame

from common import BoundingBox


class CardTypeEnum(IntEnum):
    BASIC = auto()


class CardImageEnum(IntEnum):
    BASIC_IMAGE = 1


class UIElemType(IntEnum):
    MENU = auto()
    TEXTBOX = auto()
    BUTTON = auto()
    CHECKBOX = auto()
    SLIDER = auto()


@dataclass
class UIElemSprite:
    elem_type: UIElemType
    size: Tuple[int, int]
    sub_size: Tuple[int, int] = (0, 0)
    button_data: Optional[bool | float] = None


class RenderLayerEnum(IntEnum):
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
