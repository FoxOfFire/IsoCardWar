import enum

import pygame

from common import BoundingBox


class RenderLayerEnum(enum.Enum):
    GAME = enum.auto()


def bb_to_rect(bb: BoundingBox) -> pygame.Rect:
    return pygame.Rect(bb.left, bb.top, bb.width, bb.height)
