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
    _ENUMS: Optional[List[Type[IntEnum]]] = None

    _TILE_TYPE_SURFS: List[List[pygame.Surface]] = []
    _UNIT_TYPE_SURFS: List[List[pygame.Surface]] = []
    _SELECTION_SURFS: List[List[pygame.Surface]] = []

    _COMBINDED_SURFS: Dict[
        Tuple[Optional[IntEnum], Optional[IntEnum], Optional[IntEnum]],
        List[Tuple[pygame.Surface, int, int]],
    ] = {}
    _COMBINDED_ANIM_LENS: Dict[
        Tuple[Optional[IntEnum], Optional[IntEnum], Optional[IntEnum]], int
    ] = {}

    _GENERATED_DYNAMIC_SURFS = False

    def assign_enums(self, enums: List[Type[IntEnum]]) -> None:
        self._ENUMS = enums

    def init(self) -> None:
        assert self._ENUMS is not None
        assert len(self._ENUMS) == 3
        tiles, selects, units = tuple(self._ENUMS)

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
                (selects, 0, 0),
                (units, 0, 0),
            ],
            [
                self._TILE_TYPE_SURFS,
                self._SELECTION_SURFS,
                self._UNIT_TYPE_SURFS,
            ],
        )
        assert isinstance(combinded_dict, type(self._COMBINDED_SURFS))

        self._COMBINDED_SURFS.update(combinded_dict)
        for key, val in self._COMBINDED_SURFS.items():
            self._COMBINDED_ANIM_LENS.update({key: len(val)})

        self._GENERATED_DYNAMIC_SURFS = True

    def get_surf(
        self,
        key: Tuple[Optional[IntEnum], Optional[IntEnum], Optional[IntEnum]],
        anim_offset: int,
    ) -> Tuple[pygame.Surface, int, int]:
        if not self._GENERATED_DYNAMIC_SURFS:
            self.init()

        surf_data = self._COMBINDED_SURFS[key]

        frame = ANIMATION_PROC_REF.get_frame_number(
            self._COMBINDED_ANIM_LENS[key], start_offset=anim_offset
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
