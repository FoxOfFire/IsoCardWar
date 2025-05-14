from dataclasses import dataclass
from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.iso_map import Tile

from .rendering_images import TILE_TYPES, TileTypeEnum


@dataclass
class IsoSprite:
    pass


OFFSET_X = 64
OFFSET_Y = 50


class IsoRenderer:
    def __init__(self, postrack: PositionTracker, tag: Type) -> None:
        super().__init__()
        self.postrack = postrack
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )

    def draw(self, screen: pygame.Surface) -> None:
        def sort_by_bottom(ent: int) -> int:
            tile = esper.try_component(ent, Tile)
            if tile is None:
                return -1
            return tile.x - tile.y

        ent_list = sorted(
            self.postrack.intersect(self.bb),
            key=lambda ent: sort_by_bottom(ent),
        )
        for ent in ent_list:
            if not esper.has_component(ent, IsoSprite):
                continue
            tile = esper.component_for_entity(ent, Tile)
            x = OFFSET_X + (tile.x + tile.y) * 8
            y = OFFSET_Y + (tile.x - tile.y) * 4
            screen.blit(TILE_TYPES[TileTypeEnum.BASIC], (x, y))
