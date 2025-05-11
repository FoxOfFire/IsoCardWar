from dataclasses import dataclass

import esper
import pygame

from common import BoundingBox, GameCamera, PositionTracker

from .rendering_utils import bb_to_rect


@dataclass
class GameSprite:
    color: pygame.Color


class GameRenderer:
    def __init__(self, postrack: PositionTracker) -> None:
        super().__init__()
        self.postrack = postrack
        self.bb = esper.component_for_entity(
            esper.get_component(GameCamera)[0][0],
            BoundingBox,
        )

    def Draw(self, screen: pygame.surface.Surface) -> None:
        for ent in self.postrack.intersect(self.bb):
            sprite = esper.try_component(ent, GameSprite)
            if sprite is None:
                continue
            bb = esper.component_for_entity(ent, BoundingBox)
            surf = pygame.surface.Surface((bb.width, bb.height))
            surf.fill(sprite.color)
            screen.blit(surf, bb_to_rect(bb))
