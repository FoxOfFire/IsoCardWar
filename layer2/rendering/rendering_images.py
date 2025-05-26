import enum
from pathlib import Path
from typing import Dict, List

import pygame

from layer1 import MarkerEnum
from layer1.iso_map import TerrainEnum, UnitTypeEnum


class CardTypeEnum(enum.Enum):
    BASIC = "basic"


class CardImageEnum(enum.Enum):
    BASIC = ("basic_image", 1)


BASE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets"
CARD_TYPE_ASSET_DIR = BASE_ASSET_DIR / "cards"
CARD_IMAGE_ASSET_DIR = BASE_ASSET_DIR / "card_images"
CARD_MARKER_ASSET_DIR = BASE_ASSET_DIR / "card_markers"
TILE_TYPE_ASSET_DIR = BASE_ASSET_DIR / "tiles"
UNIT_TYPE_ASSET_DIR = BASE_ASSET_DIR / "units"


CARD_TYPE_SURFS: Dict[CardTypeEnum, pygame.Surface] = {}
CARD_MARKER_SURFS: Dict[MarkerEnum, pygame.Surface] = {}
CARD_IMAGE_SURFS: Dict[CardImageEnum, List[pygame.Surface]] = {}
TILE_TYPE_SURFS: Dict[TerrainEnum, pygame.Surface] = {}
UNIT_TYPE_SURFS: Dict[UnitTypeEnum, pygame.Surface] = {}


def load_images() -> None:
    for card_type, card_type_val in [(e, e.value) for e in CardTypeEnum]:
        CARD_TYPE_SURFS.update(
            {
                card_type: pygame.image.load(
                    CARD_TYPE_ASSET_DIR / f"{card_type_val}.png"
                ).convert_alpha()
            }
        )

    for card_marker, card_marker_val in [(e, e.value) for e in MarkerEnum]:
        CARD_MARKER_SURFS.update(
            {
                card_marker: pygame.image.load(
                    CARD_MARKER_ASSET_DIR / f"marker{card_marker_val}.png"
                ).convert_alpha()
            }
        )
    for card_image, (card_image_name, card_image_frame_cnt) in [
        (e, e.value) for e in CardImageEnum
    ]:
        CARD_IMAGE_SURFS.update(
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
        TILE_TYPE_SURFS.update(
            {
                tile: pygame.image.load(
                    TILE_TYPE_ASSET_DIR / f"tiles{tile_val}.png"
                ).convert_alpha()
            }
        )
    for unit, unit_val in [(e, e.value) for e in UnitTypeEnum]:
        UNIT_TYPE_SURFS.update(
            {
                unit: pygame.image.load(
                    UNIT_TYPE_ASSET_DIR / f"units{unit_val}.png"
                ).convert_alpha()
            }
        )
