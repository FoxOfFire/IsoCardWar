from dataclasses import dataclass

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.iso_map import Tile
from layer2 import IsoCameraTag

from .rendering_utils import bb_to_rect, sorter


@dataclass
class IsoSprite:
    pass


class IsoRenderer:
    def __init__(self, postrack: PositionTracker) -> None:
        super().__init__()
        self.postrack = postrack
        self.bb = esper.component_for_entity(
            esper.get_component(IsoCameraTag)[0][0],
            BoundingBox,
        )

    def draw(self, screen: pygame.Surface) -> None:
        ent_list = sorted(
            self.postrack.intersect(self.bb),
            key=lambda ent: sorter(ent, 3),
        )
        for ent in ent_list:
            if not esper.has_component(ent, IsoSprite):
                continue
            bb = esper.component_for_entity(ent, BoundingBox)
            tile = esper.component_for_entity(ent, Tile)
            pygame.draw.rect(screen, tile.col, bb_to_rect(bb))
