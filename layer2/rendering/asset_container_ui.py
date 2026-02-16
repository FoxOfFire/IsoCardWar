from enum import IntEnum
from typing import Dict, List, Tuple

import pygame

from common import SETTINGS_REF

from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import UIElemSprite, UIElemType


class UIAssetContainer:
    _UI_ASSETS_DIR = "ui"
    _BUTTON_TILE_MAPS: Dict[IntEnum, List[pygame.Surface]] = {}
    _BUTTON_SURFS: Dict[Tuple[IntEnum, int, int], List[pygame.Surface]] = {}

    def _get_rect_tile_surf(
        self,
        enum: UIElemType,
        /,
        *,
        size: Tuple[int, int],
        offset: int,
    ) -> pygame.Surface:
        tilemap: List[pygame.Surface] = self._BUTTON_TILE_MAPS[enum]
        x, y = size
        fin = pygame.Surface(
            (
                x * SETTINGS_REF.BUTTON_TILE_SIZE,
                y * SETTINGS_REF.BUTTON_TILE_SIZE,
            ),
            flags=pygame.SRCALPHA,
        )
        fin.fill((0, 0, 0, 0))
        tilemap_len = len(tilemap)
        for i in range(x):
            for j in range(y):
                tile = (offset * 16 + 15) % tilemap_len

                if j == 0:
                    tile -= 8
                if j == y - 1:
                    tile -= 4

                if i == 0:
                    tile -= 2
                if i == x - 1:
                    tile -= 1

                surf = tilemap[tile]
                fin.blit(
                    surf,
                    surf.get_rect(
                        topleft=(
                            i * SETTINGS_REF.BUTTON_TILE_SIZE,
                            j * SETTINGS_REF.BUTTON_TILE_SIZE,
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
        assert elem != UIElemType.SLIDER
        is_checkbox = elem == UIElemType.CHECKBOX
        if is_checkbox:
            data = sprite.button_data
            assert isinstance(data, bool) and x > 1
            checksurf = self._get_checkbox_surf(data)
            elem = UIElemType.BUTTON
        surfs = self._BUTTON_SURFS.get((elem, x, y))
        if surfs is None:
            surfs = []
            for i in range(3):
                surf = self._get_rect_tile_surf(
                    elem,
                    size=(x, y),
                    offset=i,
                )
                if is_checkbox:
                    surf.blit(
                        checksurf[i], checksurf[i].get_rect(topleft=(0, 0))
                    )
                surfs.append(surf)

        return surfs

    def _load_tile_types(self) -> None:
        RENDER_ASSET_REF.load_tile_map(
            UIElemType,
            surfs=self._BUTTON_TILE_MAPS,
            path=self._UI_ASSETS_DIR,
        )

    def load_images(self) -> None:
        self._load_tile_types()


UI_ASSET_REF = UIAssetContainer()
