from typing import Dict, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker

from .card_renderer import CardRenderer
from .iso_renderer import IsoRenderer
from .rendering_utils import RenderLayerEnum


class ScreenNotFoundException(Exception):
    pass


class RenderingProcessor(esper.Processor):

    def __init__(
        self,
        display: pygame.Surface,
        layer_info: Dict[RenderLayerEnum, Tuple[PositionTracker, BoundingBox]],
        pixel_size: float,
    ) -> None:
        self.display = display

        self.screen = pygame.Surface(
            (display.get_width() / pixel_size, display.get_height() / pixel_size)
        )

        (card_postrack, card_bb) = layer_info[RenderLayerEnum.CARD]
        self.card_renderer = CardRenderer(card_postrack)
        self.card_bb = card_bb

        self.game_surf = pygame.Surface((card_bb.width, card_bb.height))

        (iso_postrack, iso_bb) = layer_info[RenderLayerEnum.ISO]
        self.iso_renderer = IsoRenderer(iso_postrack)
        self.iso_bb = iso_bb

    def process(self) -> None:

        self.screen.fill((100, 100, 100))

        self.game_surf.fill((100, 99, 101))
        self.iso_renderer.draw(self.game_surf)
        self.card_renderer.draw(self.game_surf)
        self.screen.blit(self.game_surf, self.game_surf.get_rect())

        scaled_screen = pygame.transform.scale(
            self.screen, (self.display.get_width(), self.display.get_height())
        )

        self.display.blit(scaled_screen, (0, 0))
