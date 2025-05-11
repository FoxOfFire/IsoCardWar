from typing import Dict, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker

from .card_renderer import CardRenderer
from .rendering_utils import RenderLayerEnum, bb_to_rect


class ScreenNotFoundException(Exception):
    pass


class RenderingProcessor(esper.Processor):

    def __init__(
        self,
        display: pygame.Surface,
        layer_info: Dict[RenderLayerEnum, Tuple[PositionTracker, BoundingBox]],
        pixel_size: int,
    ) -> None:
        self.display = display

        self.screen = pygame.Surface(
            (display.get_width() // pixel_size, display.get_height() // pixel_size)
        )

        (game_postrack, game_bb) = layer_info[RenderLayerEnum.GAME]
        self.game_renderer = CardRenderer(game_postrack)
        self.game_bb = game_bb
        self.game_surf = pygame.Surface((game_bb.width, game_bb.height))

    def process(self) -> None:

        self.screen.fill((100, 100, 100))

        self.game_surf.fill((0, 200, 150))
        self.game_renderer.Draw(self.game_surf)
        self.screen.blit(self.game_surf, bb_to_rect(self.game_bb))

        scaled_screen = pygame.transform.scale(
            self.screen, (self.display.get_width(), self.display.get_height())
        )

        self.display.blit(scaled_screen, (0, 0))
