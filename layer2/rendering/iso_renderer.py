from dataclasses import dataclass
from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.iso_map import Tile
from layer2.utils import (
    ISO_POS_OFFSET_X,
    ISO_POS_OFFSET_Y,
    ISO_TILE_OFFSET_X,
    ISO_TILE_OFFSET_Y,
)

from .log import logger
from .rendering_images import TILE_TYPES


@dataclass
class IsoSprite:
    pass


class IsoRenderer:
    def __init__(self, pos_track: PositionTracker, tag: Type) -> None:
        super().__init__()
        self.pos_track = pos_track
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )
        logger.info("iso renderer init finished")

    def draw(self, screen: pygame.Surface) -> None:
        def sort_by_bottom(ent: int) -> int:
            tile = esper.try_component(ent, Tile)
            if tile is None:
                return -1
            return tile.x - tile.y

        ent_list = sorted(
            self.pos_track.intersect(self.bb),
            key=lambda ent: sort_by_bottom(ent),
        )
        for ent in ent_list:
            if not esper.has_component(ent, IsoSprite):
                continue
            tile = esper.component_for_entity(ent, Tile)
            x = ISO_POS_OFFSET_X + (tile.x + tile.y) * ISO_TILE_OFFSET_X
            y = ISO_POS_OFFSET_Y + (tile.x - tile.y) * ISO_TILE_OFFSET_Y
            screen.blit(TILE_TYPES[tile.terrain], (x, y))
