from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Callable, Iterable, Optional, Tuple, Type

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
)
from layer1 import Card, Tile

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF


@dataclass
class IsoSprite:
    pass


class IsoRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self, track_tag: Type, /) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = None
        logger.info("iso renderer init finished")

    class _DrawType(IntEnum):
        TILE = auto()
        UNIT = auto()
        SELECTION = auto()

    def _draw_selection(
        self,
        screen: pygame.Surface,
        surfs: Callable[[IntEnum], pygame.Surface],
        ent: int,
        x: float,
        y: float,
    ) -> None:
        if STATE_REF.selected_card is None:
            return
        card = esper.try_component(STATE_REF.selected_card, Card)

        if ent != STATE_REF.hovered_ent or card is None:
            return

        screen.blit(surfs(card.marker), (x, y))

    def _draw_type(
        self,
        screen: pygame.Surface,
        surfs: Callable[[IntEnum], pygame.Surface],
        ent_list: Iterable[int],
        draw_type: _DrawType,
        /,
        *,
        offset: Tuple[float, float] = (0, 0),
    ) -> None:
        delta_x, delta_y = offset
        for ent in ent_list:
            if not esper.has_component(ent, IsoSprite):
                continue
            tile = esper.component_for_entity(ent, Tile)
            x = (
                delta_x
                + SETTINGS_REF.ISO_POS_OFFSET_X
                + (tile.x + tile.y) * SETTINGS_REF.ISO_TILE_OFFSET_X
            )
            y = (
                delta_y
                + SETTINGS_REF.ISO_POS_OFFSET_Y
                + (tile.x - tile.y) * SETTINGS_REF.ISO_TILE_OFFSET_Y
            )
            if ent == STATE_REF.hovered_ent:
                y += SETTINGS_REF.ISO_TILE_SELECT_OFFSET
            match draw_type:
                case self._DrawType.TILE:
                    screen.blit(surfs(tile.terrain), (x, y))

                case self._DrawType.UNIT:
                    if tile.unit is not None:
                        screen.blit(surfs(tile.unit), (x, y))

                case self._DrawType.SELECTION:
                    self._draw_selection(screen, surfs, ent, x, y)

                case _:
                    raise RuntimeError(
                        "unexpected type while drawing iso_tiles"
                    )

    def draw(self, screen: pygame.Surface) -> None:
        assert self.bb is not None

        def sort_by_bottom(ent: int) -> int:
            tile = esper.try_component(ent, Tile)
            if tile is None:
                return -1
            return tile.x - tile.y

        ent_list = sorted(
            POS_PROC_REF.intersect(self.bb, self.track_tag),
            key=lambda ent: sort_by_bottom(ent),
        )
        self._draw_type(
            screen,
            RENDER_ASSET_REF.get_tile_type_surf,
            ent_list,
            self._DrawType.TILE,
        )
        self._draw_type(
            screen,
            RENDER_ASSET_REF.get_selection_surf,
            ent_list,
            self._DrawType.SELECTION,
            offset=(0, -SETTINGS_REF.ISO_TILE_OFFSET_Y * 2),
        )
        self._draw_type(
            screen,
            RENDER_ASSET_REF.get_unit_type_surf,
            ent_list,
            self._DrawType.UNIT,
            offset=(0, -SETTINGS_REF.ISO_TILE_OFFSET_Y * 2),
        )
