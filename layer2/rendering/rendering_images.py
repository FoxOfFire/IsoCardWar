import enum
from pathlib import Path
from typing import Dict, List

import pygame

from layer1 import MarkerEnum
from layer1.iso_map import TerrainEnum


class CardTypeEnum(enum.Enum):
    BASIC = "basic"


class CardImageEnum(enum.Enum):
    BASIC = ("basic_image", 1)


CARD_TYPE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "cards"
CARD_IMAGE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "card_images"
CARD_MARKER_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "card_markers"
TILE_TYPE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets" / "tiles"


CARD_TYPES: Dict[CardTypeEnum, pygame.Surface] = {}
CARD_MARKERS: Dict[MarkerEnum, pygame.Surface] = {}
CARD_IMAGES: Dict[CardImageEnum, List[pygame.Surface]] = {}
TILE_TYPES: Dict[TerrainEnum, pygame.Surface] = {}


def load_images() -> None:
    for card_type, card_type_val in [(e, e.value) for e in CardTypeEnum]:
        CARD_TYPES.update(
            {
                card_type: pygame.image.load(
                    CARD_TYPE_ASSET_DIR / f"{card_type_val}.png"
                ).convert_alpha()
            }
        )

    for card_marker, card_marker_val in [(e, e.value) for e in MarkerEnum]:
        CARD_MARKERS.update(
            {
                card_marker: pygame.image.load(
                    CARD_MARKER_ASSET_DIR / f"marker{card_marker_val}.png"
                ).convert_alpha()
            }
        )
    for card_image, (card_image_name, card_image_frame_cnt) in [
        (e, e.value) for e in CardImageEnum
    ]:
        CARD_IMAGES.update(
            {
                card_image: [
                    pygame.image.load(
                        CARD_IMAGE_ASSET_DIR
                        / f"{card_image_name}"
                        / f"card_{card_image_name}{i+1}.png"
                    ).convert_alpha()
                    for i in range(card_image_frame_cnt)
                ]
            }
        )

    for tile, tile_val in [(e, e.value) for e in TerrainEnum]:
        TILE_TYPES.update(
            {
                tile: pygame.image.load(
                    TILE_TYPE_ASSET_DIR / f"tiles{tile_val}.png"
                ).convert_alpha()
            }
        )
