from enum import IntEnum
from typing import Dict, Optional, Tuple

import pygame

from common import SETTINGS_REF, PriceEnum
from layer1 import TerrainEnum, UnitTypeEnum

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF


class IsoAssetContainer:

    _ISO_ASSETS_DIR = "iso"
    _ISO_MASK: Optional[pygame.Mask] = None
    _TILE_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _UNIT_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _SELECTION_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _COMBINDED_SURFS: Dict[
        Tuple[IntEnum, Optional[IntEnum], Optional[IntEnum]], pygame.Surface
    ] = {}
    _LOADED_IMAGES: bool = False

    def get_surf(
        self, tile: IntEnum, unit: Optional[IntEnum], select: Optional[IntEnum]
    ) -> pygame.Surface:
        surf = self._COMBINDED_SURFS.get((tile, unit, select))
        if surf is None:
            if not self._LOADED_IMAGES:
                if SETTINGS_REF.LOG_ASSET_LOADING:
                    logger.info("Loaded base images")
                self._load_image_types()
                self._LOADED_IMAGES = True

            surf = pygame.Surface(
                (
                    SETTINGS_REF.ISO_TILE_SPRITE_WIDTH,
                    SETTINGS_REF.ISO_TILE_SPRITE_HEIGHT,
                ),
                flags=pygame.SRCALPHA,
            )

            t_surf = self._TILE_TYPE_SURFS[tile]
            t_offset = SETTINGS_REF.ISO_TILE_OFFSET_Y * 2
            t_rect = t_surf.get_rect(topleft=(0, t_offset))
            surf.blit(t_surf, t_rect)

            if select is not None:
                s_surf = self._SELECTION_SURFS[select]
                s_rect = s_surf.get_rect(topleft=(0, 0))
                surf.blit(s_surf, s_rect)

            if unit is not None:
                u_surf = self._UNIT_TYPE_SURFS[unit]
                u_rect = u_surf.get_rect(topleft=(0, 0))
                surf.blit(u_surf, u_rect)

            if SETTINGS_REF.LOG_ASSET_LOADING:
                logger.info(f"added tile sprite: {tile.name, unit, select}")
            self._COMBINDED_SURFS.update({(tile, unit, select): surf})
        return surf

    def get_mask(self) -> pygame.Mask:
        if self._ISO_MASK is None:
            mask_surf = RENDER_ASSET_REF.load_single_image(
                self._ISO_ASSETS_DIR, "tile_mask"
            ).convert_alpha()
            mask = pygame.mask.from_surface(mask_surf)
            self._ISO_MASK = mask
        return self._ISO_MASK.copy()

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
            PriceEnum,
            surfs=self._SELECTION_SURFS,
            path=self._ISO_ASSETS_DIR,
        )


ISO_ASSET_REF = IsoAssetContainer()
