from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Type

import pygame

from common.constants import FONT_SIZE
from layer1 import MarkerEnum
from layer1.iso_map import SelectionTypeEnum, TerrainEnum, UnitTypeEnum

from .log import logger


class CardTypeEnum(Enum):
    BASIC = "basic"


class CardImageEnum(Enum):
    BASIC = ("basic_image", 1)


class UIElemType(Enum):
    BUTTON = ("button", 3)
    TEXTBOX = ("textbox", 3)


BASE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets"
CARD_TYPE_ASSET_DIR = BASE_ASSET_DIR / "cards" / "card_frames"
CARD_IMAGE_ASSET_DIR = BASE_ASSET_DIR / "cards" / "card_images"
CARD_MARKER_ASSET_DIR = BASE_ASSET_DIR / "cards" / "card_markers"
SELECTION_ASSET_DIR = BASE_ASSET_DIR / "iso" / "tile_selections"
TILE_TYPE_ASSET_DIR = BASE_ASSET_DIR / "iso" / "tiles"
UNIT_TYPE_ASSET_DIR = BASE_ASSET_DIR / "iso" / "units"
FONT_ASSET_DIR = BASE_ASSET_DIR / "fonts"
BUTTON_ASSET_DIR = BASE_ASSET_DIR / "ui"


CARD_TYPE_SURFS: Dict[Enum, pygame.Surface] = {}
CARD_MARKER_SURFS: Dict[Enum, pygame.Surface] = {}
CARD_IMAGE_SURFS: Dict[Enum, List[pygame.Surface]] = {}
TILE_TYPE_SURFS: Dict[Enum, pygame.Surface] = {}
UNIT_TYPE_SURFS: Dict[Enum, pygame.Surface] = {}
SELECTION_SURFS: Dict[Enum, pygame.Surface] = {}
BUTTON_SURFS: Dict[Enum, List[pygame.Surface]] = {}


@dataclass
class _FontContainer:
    font: Optional[pygame.font.Font] = None


_font_container = _FontContainer()


def get_font() -> pygame.font.Font:
    if _font_container.font is None:
        logger.info("loaded font")
        _font_container.font = pygame.font.Font(FONT_ASSET_DIR / "tiny.ttf", FONT_SIZE)
    return _font_container.font


def _load_image_type(
    enum: Type[Enum], surfs: Dict[Enum, pygame.Surface], path: Path, name: str
) -> None:
    logger.info(f"loaded image assets of type:{enum}")
    for type, val in [(e, e.value) for e in enum]:
        surfs.update(
            {type: pygame.image.load(path / f"{name}{val}.png").convert_alpha()}
        )


def _load_animation_type(
    enum: Type[Enum], surfs: Dict[Enum, List[pygame.Surface]], path: Path, name: str
) -> None:
    logger.info(f"loaded animation assets of type: {enum}")
    for images, (img_name, frame_cnt) in [(e, e.value) for e in enum]:
        surfs.update(
            {
                images: [
                    pygame.image.load(
                        path / f"{img_name}" / f"{name}{img_name}{i+1}.png"
                    ).convert_alpha()
                    for i in range(frame_cnt)
                ]
            }
        )


def load_images() -> None:
    _load_image_type(CardTypeEnum, CARD_TYPE_SURFS, CARD_TYPE_ASSET_DIR, "")
    _load_image_type(MarkerEnum, CARD_MARKER_SURFS, CARD_MARKER_ASSET_DIR, "marker")
    _load_image_type(TerrainEnum, TILE_TYPE_SURFS, TILE_TYPE_ASSET_DIR, "tiles")
    _load_image_type(UnitTypeEnum, UNIT_TYPE_SURFS, UNIT_TYPE_ASSET_DIR, "units")
    _load_image_type(
        SelectionTypeEnum, SELECTION_SURFS, SELECTION_ASSET_DIR, "tile_selections"
    )

    _load_animation_type(CardImageEnum, CARD_IMAGE_SURFS, CARD_IMAGE_ASSET_DIR, "card_")
    _load_animation_type(UIElemType, BUTTON_SURFS, BUTTON_ASSET_DIR, "")
