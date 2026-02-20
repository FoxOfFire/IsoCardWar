from enum import IntEnum
from typing import Dict, List, Optional, Tuple

import pygame

from common import SETTINGS_REF

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import UIElemSprite, UIElemType


class UIAssetContainer:
    _UI_ASSETS_DIR = "ui"
    _BUTTON_TILE_MAPS: Dict[IntEnum, List[pygame.Surface]] = {}
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
        fin.fill((0, 0, 0, 0))
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

    def _get_checkbox_surf(self, checked: bool) -> List[pygame.Surface]:
        pos = 0
        if checked:
            pos += 3
        tiles = self._BUTTON_TILE_MAPS[UIElemType.CHECKBOX]
        ret = []
        for i in range(pos, pos + 3):
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
                checksurf = self._get_checkbox_surf(data)
                elem = UIElemType.BUTTON
            surfs = []
            for i in range(3):
                surf = self._get_rect_tile_surf(
                    elem, (x, y), i, sprite.sub_size
                )
                if is_checkbox:
                    surf.blit(
                        checksurf[i], checksurf[i].get_rect(topleft=(0, 0))
                    )
                surfs.append(surf)
            if is_checkbox:
                elem = UIElemType.CHECKBOX

            if SETTINGS_REF.LOG_ASSET_LOADING:
                logger.info(f"updated button:{elem, data, x, y}")
            self._BUTTON_SURFS.update(
                {(elem, data, (x, y), sprite.sub_size): surfs}
            )

        return surfs

    def _load_tile_types(self) -> None:
        RENDER_ASSET_REF.load_tile_map(
            UIElemType,
            surfs=self._BUTTON_TILE_MAPS,
            path=self._UI_ASSETS_DIR,
        )


UI_ASSET_REF = UIAssetContainer()
