from typing import Optional, Tuple, Type

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
    PriceEnum,
)
from layer1 import Card, Tile
from layer2.tags import MaskedSprite

from .asset_container_iso import ISO_ASSET_REF
from .log import logger


class IsoRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        cams = esper.get_component(cam_tag)
        if len(cams) > 0:
            self.bb = esper.component_for_entity(cams[0][0], BoundingBox)

    def __init__(self) -> None:
        super().__init__()
        self.bb = None
        logger.info("iso renderer init finished")

    def _get_selection(self) -> Optional[Tuple[int, bool]]:
        hovered_ent = STATE_REF.hovered_ent
        selected_card = STATE_REF.selected_card
        if hovered_ent is None:
            return None
        if selected_card is None:
            return hovered_ent, False
        card = esper.try_component(selected_card, Card)
        return hovered_ent, card is not None

    def draw(self, screen: pygame.Surface) -> None:
        if self.bb is None:
            return

        def filterer(ent: int) -> bool:
            mask = esper.has_component(ent, MaskedSprite)
            tile = esper.has_component(ent, Tile)
            return mask and tile

        def sort_by_bottom(ent: int) -> int:
            tile = esper.component_for_entity(ent, Tile)
            return tile.x - tile.y

        ent_list = POS_PROC_REF().intersect(self.bb)
        ent_list = sorted(filter(filterer, ent_list), key=sort_by_bottom)

        crosshair = None
        maybe_selected = self._get_selection()
        if maybe_selected is None:
            selected = -1
        else:
            selected, marked = maybe_selected
            if marked:
                crosshair = PriceEnum.MANA

        for ent in ent_list:
            sprite = esper.component_for_entity(ent, MaskedSprite)
            tile = esper.component_for_entity(ent, Tile)
            x, y = tile.offset
            if ent != selected:
                if tile.is_targeted:
                    select = PriceEnum.BLOOD
                else:
                    select = None
                y -= SETTINGS_REF.ISO_TILE_SELECT_OFFSET
            else:
                if crosshair is not None:
                    select = crosshair
                elif tile.is_targeted:
                    select = PriceEnum.BLOOD
            surf = ISO_ASSET_REF.get_surf(tile.terrain, tile.unit, select)
            sprite.mask = ISO_ASSET_REF.get_mask()

            screen.blit(surf, (x, y))
