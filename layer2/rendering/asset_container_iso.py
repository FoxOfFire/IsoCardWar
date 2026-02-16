from enum import IntEnum
from typing import Dict

import pygame

from common import MarkerEnum
from layer1 import TerrainEnum, UnitTypeEnum

from .rendering_asset_loader import RENDER_ASSET_REF


class IsoAssetContainer:

    _ISO_ASSETS_DIR = "iso"
    _TILE_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _UNIT_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _SELECTION_SURFS: Dict[IntEnum, pygame.Surface] = {}

    def get_tile_type_surf(self, t: IntEnum) -> pygame.Surface:
        return self._TILE_TYPE_SURFS[t]

    def get_unit_type_surf(self, t: IntEnum) -> pygame.Surface:
        return self._UNIT_TYPE_SURFS[t]

    def get_selection_surf(self, t: IntEnum) -> pygame.Surface:
        return self._SELECTION_SURFS[t]

    def _load_image_types(self) -> None:
        RENDER_ASSET_REF.load_image_type(
            TerrainEnum,
            surfs=self._TILE_TYPE_SURFS,
            path=self._ISO_ASSETS_DIR,
        )
        RENDER_ASSET_REF.load_image_type(
            UnitTypeEnum,
            surfs=self._UNIT_TYPE_SURFS,
            path=self._ISO_ASSETS_DIR,
        )
        RENDER_ASSET_REF.load_image_type(
            MarkerEnum,
            surfs=self._SELECTION_SURFS,
            path=self._ISO_ASSETS_DIR,
        )

    def load_images(self) -> None:
        self._load_image_types()


ISO_ASSET_REF = IsoAssetContainer()
