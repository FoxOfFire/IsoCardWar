from enum import IntEnum
from typing import Dict, List, Optional, Tuple

import pygame

from common import COLOR_REF, SETTINGS_REF, PriceEnum

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import UIElemSprite, UIElemType


class UIAssetContainer:
    _UI_ASSETS_DIR = "ui"
    _BUTTON_TILE_MAPS: Dict[IntEnum, List[pygame.Surface]] = {}
    _ICON_SURFS: List[pygame.Surface] = []
    _ICON_BACKGROUND_SURFS: List[pygame.Surface] = []
    _LOADED_TILE_MAPS: bool = False
    _BUTTON_SURFS: Dict[
        Tuple[
            IntEnum, Optional[float | bool], Tuple[int, int], Tuple[int, int]
        ],
        List[pygame.Surface],
    ] = {}

    def _get_rect_tile_surf(
        self,
        enum: UIElemType,
        size: Tuple[int, int],
        offset: int,
        sub_size: Tuple[int, int] = (0, 0),
    ) -> pygame.Surface:
        tilemap: List[pygame.Surface] = self._BUTTON_TILE_MAPS[enum]
        x, y = size
        sub_x, sub_y = sub_size
        flag_x, flag_y = sub_x > 0, sub_y > 0
        assert sub_x >= 0 and sub_y >= 0
        fin = pygame.Surface(
            (
                x * SETTINGS_REF.BUTTON_TILE_SIZE + sub_x,
                y * SETTINGS_REF.BUTTON_TILE_SIZE + sub_y,
            ),
            flags=pygame.SRCALPHA,
        )
        fin.fill(COLOR_REF.TRANSPARENT)
        tilemap_len = len(tilemap)
        if flag_x:
            x += 1
        if flag_y:
            y += 1
        for i in range(x):
            i_offset = 0
            i_sub_offset = 0
            if i == 0:
                i_offset += 2
            if i == x - 1:
                i_offset += 1
                if flag_x:
                    i_sub_offset = SETTINGS_REF.BUTTON_TILE_SIZE - sub_x

            for j in range(y):
                tile = (offset * 16 + 15) % tilemap_len
                j_sub_offset = 0

                if j == 0:
                    tile -= 8
                if j == y - 1:
                    tile -= 4
                    if flag_y:
                        j_sub_offset = SETTINGS_REF.BUTTON_TILE_SIZE - sub_y

                tile -= i_offset

                surf = tilemap[tile]
                fin.blit(
                    surf,
                    surf.get_rect(
                        topleft=(
                            i * SETTINGS_REF.BUTTON_TILE_SIZE - i_sub_offset,
                            j * SETTINGS_REF.BUTTON_TILE_SIZE - j_sub_offset,
                        )
                    ),
                )
        return fin

    def _get_icon_surf(
        self, icon_type: UIElemType, offset: int
    ) -> List[pygame.Surface]:
        tiles = self._BUTTON_TILE_MAPS[icon_type]
        ret = []
        for i in range(3 * offset, 3 * (offset + 1)):
            ret.append(tiles[i])
        return ret

    def get_button_surf(self, sprite: UIElemSprite) -> List[pygame.Surface]:
        elem = sprite.elem_type
        x, y = sprite.size
        data = sprite.button_data

        if elem == UIElemType.SLIDER:
            data = None
            assert x == 1 or y == 1
        surfs = self._BUTTON_SURFS.get((elem, data, (x, y), sprite.sub_size))
        if surfs is None:
            if not self._LOADED_TILE_MAPS:
                self._load_tile_types()
                self._LOADED_TILE_MAPS = True
                if SETTINGS_REF.LOG_ASSET_LOADING:
                    logger.info("loaded ui tile maps")

            is_checkbox = elem == UIElemType.CHECKBOX
            if is_checkbox:
                assert isinstance(data, bool)
                offset = 0 if data else 1
                checksurf = self._get_icon_surf(elem, offset)
                elem = UIElemType.BUTTON

            is_icon = elem == UIElemType.ICON
            if is_icon:
                assert isinstance(data, int)
                icon_surf = self._get_icon_surf(elem, data)
                elem = UIElemType.TEXTBOX

            surfs = []
            for i in range(3):
                surf = self._get_rect_tile_surf(
                    elem, (x, y), i, sprite.sub_size
                )

                if is_checkbox:
                    surf.blit(checksurf[i])
                if is_icon:
                    surf.blit(icon_surf[i])

                surfs.append(surf)
            if is_checkbox:
                elem = UIElemType.CHECKBOX
            if is_icon:
                elem = UIElemType.ICON

            if SETTINGS_REF.LOG_ASSET_LOADING:
                logger.info(f"updated button:{elem, data, x, y}")
            self._BUTTON_SURFS.update(
                {(elem, data, (x, y), sprite.sub_size): surfs}
            )

        return surfs

    def _load_checkbox_tiles(
        self, checkbox_icon_num: int, background: int
    ) -> None:
        surfs: List[pygame.Surface] = []
        for i in range(3):
            surf = self._ICON_BACKGROUND_SURFS[i + background * 3].copy()
            surf.blit(self._ICON_SURFS[checkbox_icon_num])
            surfs.append(surf)
        for i in range(3):
            surfs.append(self._ICON_BACKGROUND_SURFS[i].copy())
        self._BUTTON_TILE_MAPS.update({UIElemType.CHECKBOX: surfs})

    def _load_icon_tiles(self, icon_start: int, background: int) -> None:
        surfs: List[pygame.Surface] = []
        for resource in PriceEnum:
            for i in range(3):
                surf = self._ICON_BACKGROUND_SURFS[i + background * 3].copy()
                surf.blit(self._ICON_SURFS[icon_start + resource.value - 1])
                surfs.append(surf)
        self._BUTTON_TILE_MAPS.update({UIElemType.ICON: surfs})

    def _load_tile_types(self) -> None:
        RENDER_ASSET_REF.load_tile_map_enum(
            UIElemType,
            surfs=self._BUTTON_TILE_MAPS,
            path=self._UI_ASSETS_DIR,
        )
        self._ICON_BACKGROUND_SURFS = RENDER_ASSET_REF.load_tile_map(
            self._UI_ASSETS_DIR, "icon_backgrounds"
        )
        self._ICON_SURFS = RENDER_ASSET_REF.load_tile_map(
            self._UI_ASSETS_DIR, "icons"
        )
        logger.info(len(self._ICON_BACKGROUND_SURFS))
        self._load_checkbox_tiles(0, 0)
        self._load_icon_tiles(1, 1)


UI_ASSET_REF = UIAssetContainer()
