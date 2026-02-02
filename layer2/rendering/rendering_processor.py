from typing import Dict, Tuple, Type

import esper
import pygame

from common import BoundingBox, PositionProcessor
from common.constants import GAME_CAM_HEIGHT, GAME_CAM_WIDTH
from layer2 import GameCameraTag, IsoCameraTag, TrackIso, TrackUI

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
        layer_info: Dict[RenderLayerEnum, BoundingBox],
        pos_track: PositionProcessor,
    ) -> None:
        self.display = display

        self.screen = pygame.Surface((GAME_CAM_WIDTH, GAME_CAM_HEIGHT))

        card_bb = layer_info[RenderLayerEnum.CARD]
        iso_bb = layer_info[RenderLayerEnum.ISO]

        self.card_bb = card_bb
        self.iso_bb = iso_bb

        self.card_renderer = CardRenderer(pos_track, GameCameraTag, TrackUI)
        self.iso_renderer = IsoRenderer(pos_track, IsoCameraTag, TrackIso)
        self.mask_renderer = MaskRenderer(pos_track, GameCameraTag, TrackUI)
        self.button_renderer = ButtonRenderer(pos_track, GameCameraTag, TrackUI)

        # debug purposes
        self.bb_renderer = BBRenderer(pos_track, GameCameraTag, TrackUI)

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
