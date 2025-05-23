import enum

import esper
import pygame

from common import BoundingBox

RELATIVE_MARKER_POS_X = 2
RELATIVE_MARKER_POS_Y = 2


class RenderLayerEnum(enum.Enum):
    CARD = enum.auto()
    ISO = enum.auto()


def bb_to_rect(bb: BoundingBox) -> pygame.Rect:
    return pygame.Rect(bb.left, bb.top, bb.width, bb.height)


def sort_by_bb(ent: int, side: int) -> float:
    """
    0-left 1-right 2-top 3-bottom
    """
    return esper.component_for_entity(ent, BoundingBox).points[side]
