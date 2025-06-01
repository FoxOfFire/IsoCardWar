from typing import Dict, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker
from common.constants import GAME_CAM_HEIGHT, GAME_CAM_WIDTH
from layer2 import GameCameraTag, IsoCameraTag

from .renderer_bb import BBRenderer
from .renderer_button import ButtonRenderer
from .renderer_card import CardRenderer
from .renderer_iso import IsoRenderer
from .renderer_mask import MaskRenderer
from .utils import RenderLayerEnum


class ScreenNotFoundException(Exception):
    pass


class RenderingProcessor(esper.Processor):

    def __init__(
        self,
        display: pygame.Surface,
        layer_info: Dict[RenderLayerEnum, Tuple[PositionTracker, BoundingBox]],
    ) -> None:
        self.display = display

        self.screen = pygame.Surface((GAME_CAM_WIDTH, GAME_CAM_HEIGHT))

        (card_pos_track, card_bb) = layer_info[RenderLayerEnum.CARD]
        (iso_pos_track, iso_bb) = layer_info[RenderLayerEnum.ISO]

        self.card_bb = card_bb
        self.iso_bb = iso_bb

        self.card_renderer = CardRenderer(card_pos_track, GameCameraTag)
        self.iso_renderer = IsoRenderer(iso_pos_track, IsoCameraTag)
        self.mask_renderer = MaskRenderer(card_pos_track, GameCameraTag)
        self.button_renderer = ButtonRenderer(card_pos_track, GameCameraTag)

        # debug purposes
        self.bb_renderer = BBRenderer(card_pos_track, GameCameraTag)

    def process(self) -> None:

        self.screen.fill((100, 100, 100))

        self.iso_renderer.draw(self.screen)
        self.card_renderer.draw(self.screen)
        self.mask_renderer.draw(self.screen)
        self.button_renderer.draw(self.screen)
        self.bb_renderer.draw(self.screen)

        scaled_screen = pygame.transform.scale(
            self.screen, (self.display.get_width(), self.display.get_height())
        )

        self.display.blit(scaled_screen, scaled_screen.get_rect(topleft=(0, 0)))
