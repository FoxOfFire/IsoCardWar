from typing import Optional

import esper
import pygame

from common import SETTINGS_REF
from layer2.tags import GameCameraTag, IsoCameraTag, TrackIso, TrackUI

from .log import logger
from .renderer_bb import BBRenderer
from .renderer_button import ButtonRenderer
from .renderer_card import CardRenderer
from .renderer_iso import IsoRenderer
from .renderer_mask import MaskRenderer


class ScreenNotFoundException(Exception):
    pass


class RenderingProcessor(esper.Processor):

    display: Optional[pygame.Surface]

    def __init__(
        self,
    ) -> None:
        self.display = None

        self.screen = pygame.Surface(
            (SETTINGS_REF.GAME_CAM_WIDTH, SETTINGS_REF.GAME_CAM_HEIGHT)
        )

        self.iso_renderer = IsoRenderer(TrackIso)
        self.card_renderer = CardRenderer(TrackUI)
        self.mask_renderer = MaskRenderer(TrackUI)
        self.button_renderer = ButtonRenderer(TrackUI)

        # debug purposes
        if SETTINGS_REF.RENDER_BBS:
            self.bb_renderer = BBRenderer(GameCameraTag, TrackUI)

    def init(self, display: pygame.Surface) -> None:
        self.__set_display(display)
        self.__set_camera_types()

    def __set_display(self, display: pygame.Surface) -> None:
        self.display = display
        logger.info("display set")

    def __set_camera_types(self) -> None:
        self.iso_renderer.set_camera_type(IsoCameraTag)
        self.mask_renderer.set_camera_type(GameCameraTag)
        self.card_renderer.set_camera_type(GameCameraTag)
        self.button_renderer.set_camera_type(GameCameraTag)
        logger.info("cameras set")

    def process(self) -> None:
        assert self.display is not None

        self.screen.fill((100, 100, 100))

        self.iso_renderer.draw(self.screen)
        self.card_renderer.draw(self.screen)
        self.mask_renderer.draw(self.screen)
        self.button_renderer.draw(self.screen)

        # debug purposes
        if SETTINGS_REF.RENDER_BBS:
            self.bb_renderer.draw(self.screen)

        scaled_screen = pygame.transform.scale(
            self.screen, (self.display.get_width(), self.display.get_height())
        )

        self.display.blit(
            scaled_screen, scaled_screen.get_rect(topleft=(0, 0))
        )


RENDER_PROC_REF = RenderingProcessor()
