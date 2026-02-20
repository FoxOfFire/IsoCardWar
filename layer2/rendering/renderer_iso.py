from dataclasses import dataclass
from typing import Optional, Tuple, Type

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
    MarkerEnum,
)
from layer1 import Card, Tile

from .asset_container_iso import ISO_ASSET_REF
from .log import logger


@dataclass
class IsoSprite:
    pass


class IsoRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        cams = esper.get_component(cam_tag)
        if len(cams) > 0:
            self.bb = esper.component_for_entity(cams[0][0], BoundingBox)

    def __init__(self, track_tag: Type, /) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = None
        logger.info("iso renderer init finished")

    def _get_selection(
        self,
    ) -> Optional[Tuple[int, Optional[MarkerEnum]]]:
        hovered_ent = STATE_REF.hovered_ent
        selected_card = STATE_REF.selected_card
        if hovered_ent is None:
            return None
        if selected_card is None:
            return hovered_ent, None
        card = esper.try_component(selected_card, Card)
        if card is None:
            return hovered_ent, None
        return hovered_ent, card.marker

    def draw(self, screen: pygame.Surface) -> None:
        if self.bb is None:
            return

        def sort_by_bottom(ent: int) -> int:
            tile = esper.try_component(ent, Tile)
            if tile is None:
                return -1
            return tile.x - tile.y

        ent_list = sorted(
            POS_PROC_REF().intersect(self.bb, self.track_tag),
            key=lambda ent: sort_by_bottom(ent),
        )

        maybe_select = self._get_selection()
        if maybe_select is None:
            selected, marker = -1, None
        else:
            selected, marker = maybe_select

        for ent in ent_list:
            if not esper.has_component(ent, IsoSprite):
                continue
            tile = esper.component_for_entity(ent, Tile)
            x = (
                SETTINGS_REF.ISO_POS_OFFSET_X
                + (tile.x + tile.y) * SETTINGS_REF.ISO_TILE_OFFSET_X
            )
            y = (
                SETTINGS_REF.ISO_POS_OFFSET_Y
                + (tile.x - tile.y - 2) * SETTINGS_REF.ISO_TILE_OFFSET_Y
            )
            if ent == selected:
                select = marker
            else:
                y -= SETTINGS_REF.ISO_TILE_SELECT_OFFSET
                select = None
            surf = ISO_ASSET_REF.get_surf(tile.terrain, tile.unit, select)

            screen.blit(surf, (x, y))
