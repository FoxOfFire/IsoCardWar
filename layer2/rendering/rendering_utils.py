import enum
from pathlib import Path
from typing import Dict, List

import pygame

from common import BoundingBox


class CardTypeEnum(enum.Enum):
    BASIC = "basic"


class CardImageEnum(enum.Enum):
    BASIC = ("basic_image", 1)


CARD_TYPE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "cards"
CARD_IMAGE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "card_images"

CARD_TYPES: Dict[CardTypeEnum, pygame.Surface] = {}
CARD_IMAGES: Dict[CardImageEnum, List[pygame.Surface]] = {}


def load_images() -> None:
    for t_val, t_name in [(e, e.value) for e in CardTypeEnum]:
        CARD_TYPES.update(
            {
                t_val: pygame.image.load(
                    CARD_TYPE_ASSET_DIR / f"{t_name}.png"
                ).convert_alpha()
            }
        )
    for i_val, (i_name, i_frame_cnt) in [(e, e.value) for e in CardImageEnum]:
        CARD_IMAGES.update(
            {
                i_val: [
                    pygame.image.load(
                        CARD_IMAGE_ASSET_DIR / f"{i_name}" / f"card_{i_name}{i+1}.png"
                    ).convert_alpha()
                    for i in range(i_frame_cnt)
                ]
            }
        )


class RenderLayerEnum(enum.Enum):
    GAME = enum.auto()


def bb_to_rect(bb: BoundingBox) -> pygame.Rect:
    return pygame.Rect(bb.left, bb.top, bb.width, bb.height)
