import enum
from pathlib import Path
from typing import Dict, List

import pygame


class CardTypeEnum(enum.Enum):
    BASIC = "basic"


class CardImageEnum(enum.Enum):
    BASIC = ("basic_image", 1)


class TileTypeEnum(enum.Enum):
    BASIC = "basic"


CARD_TYPE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "cards"
CARD_IMAGE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "card_images"
TILE_TYPE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "tiles"

CARD_TYPES: Dict[CardTypeEnum, pygame.Surface] = {}
CARD_IMAGES: Dict[CardImageEnum, List[pygame.Surface]] = {}
TILE_TYPES: Dict[TileTypeEnum, pygame.Surface] = {}


def load_images() -> None:
    for card_type_val, card_type_name in [(e, e.value) for e in CardTypeEnum]:
        CARD_TYPES.update(
            {
                card_type_val: pygame.image.load(
                    CARD_TYPE_ASSET_DIR / f"{card_type_name}.png"
                ).convert_alpha()
            }
        )
    for card_image_val, (card_image_name, card_image_frame_cnt) in [
        (e, e.value) for e in CardImageEnum
    ]:
        CARD_IMAGES.update(
            {
                card_image_val: [
                    pygame.image.load(
                        CARD_IMAGE_ASSET_DIR
                        / f"{card_image_name}"
                        / f"card_{card_image_name}{i+1}.png"
                    ).convert_alpha()
                    for i in range(card_image_frame_cnt)
                ]
            }
        )

    for tile_val, tile_name in [(e, e.value) for e in TileTypeEnum]:
        TILE_TYPES.update(
            {
                tile_val: pygame.image.load(
                    TILE_TYPE_ASSET_DIR / f"{tile_name}.png"
                ).convert_alpha()
            }
        )
