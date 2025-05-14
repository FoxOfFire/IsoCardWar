import enum
from typing import Tuple

import esper
import pygame

from common import BoundingBox


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


class MaskedSprite:
    mask: pygame.Mask = pygame.Mask((1, 1), fill=True)
    rect: pygame.Rect = pygame.Rect(0, 0, 1, 1)
    mask_offset: Tuple[float, float]
