from enum import IntEnum
from typing import Dict, List, Optional, Tuple, Type

import pygame

from common import SETTINGS_REF

from .animation_processor import ANIMATION_PROC_REF
from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF


class IsoAssetContainer:

    _ISO_ASSETS_DIR = "iso"
    _ISO_MASK: Optional[pygame.Mask] = None
    _TILE_TYPE_SURFS: List[List[pygame.Surface]] = []
    _UNIT_TYPE_SURFS: List[List[pygame.Surface]] = []
    _SELECTION_SURFS: List[List[pygame.Surface]] = []
    _COMBINDED_SURFS: Dict[
        Tuple[Optional[IntEnum], Optional[IntEnum], Optional[IntEnum]],
        List[pygame.Surface],
    ] = {}
    _LOADED_IMAGES: bool = False
    _GENERATED_DYNAMIC_SURFS = False

    def init(
        self,
        tiles: Type[IntEnum],
        units: Type[IntEnum],
        selects: Type[IntEnum],
    ) -> None:
        if self._GENERATED_DYNAMIC_SURFS:
            return
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info("Loaded base images")
        self._load_image_types()
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info("Combining iso animation surfs")
        combinded_dict = RENDER_ASSET_REF.create_animation(
            (
                SETTINGS_REF.ISO_TILE_SPRITE_WIDTH,
                SETTINGS_REF.ISO_TILE_SPRITE_HEIGHT,
            ),
            [
                (tiles, 0, SETTINGS_REF.ISO_TILE_OFFSET_Y * 2),
                (units, 0, 0),
                (selects, 0, 0),
            ],
            [
                self._TILE_TYPE_SURFS,
                self._UNIT_TYPE_SURFS,
                self._SELECTION_SURFS,
            ],
        )
        assert isinstance(combinded_dict, type(self._COMBINDED_SURFS))

        self._COMBINDED_SURFS.update(combinded_dict)
        self._GENERATED_DYNAMIC_SURFS = True

    def get_surf(
        self,
        tile: IntEnum,
        unit: Optional[IntEnum],
        select: Optional[IntEnum],
        anim_offset: int,
    ) -> pygame.Surface:
        surf_data = self._COMBINDED_SURFS.get((tile, unit, select))
        assert surf_data is not None
        frame = (ANIMATION_PROC_REF.get_frame_number() + anim_offset) % len(
            surf_data
        )
        return surf_data[frame]

    def get_mask(self) -> pygame.Mask:
        if self._ISO_MASK is None:
            mask_surf = RENDER_ASSET_REF.load_tile_map(
                self._ISO_ASSETS_DIR, "tile_mask"
            )[0][0].convert_alpha()
            mask = pygame.mask.from_surface(mask_surf)
            self._ISO_MASK = mask
        return self._ISO_MASK.copy()

    def _load_image_types(self) -> None:

        self._TILE_TYPE_SURFS += RENDER_ASSET_REF.load_tile_map(
            self._ISO_ASSETS_DIR, "tiles"
        )
        self._UNIT_TYPE_SURFS += RENDER_ASSET_REF.load_tile_map(
            self._ISO_ASSETS_DIR, "units"
        )
        self._SELECTION_SURFS += RENDER_ASSET_REF.load_tile_map(
            self._ISO_ASSETS_DIR, "tile_selections"
        )


ISO_ASSET_REF = IsoAssetContainer()
