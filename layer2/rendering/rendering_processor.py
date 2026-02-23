from typing import Dict, Optional

import esper
import pygame

from common import SETTINGS_REF, WORLD_REF, WorldEnum
from layer2.tags import GameCameraTag, IsoCameraTag, TrackIso, TrackUI

from .log import logger
from .render_particle import ParticleRenderer
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
        self.particle_renderer = ParticleRenderer(TrackUI)

        # debug purposes
        if SETTINGS_REF.RENDER_BBS:
            self.bb_renderer = BBRenderer(GameCameraTag, TrackUI)

    def set_display_and_init_cam_types(self, display: pygame.Surface) -> None:
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
        self.particle_renderer.set_camera_type(GameCameraTag)
        logger.info("cameras set")

    def process(self) -> None:
        assert self.display is not None

        self.screen.fill((100, 100, 100))

        self.iso_renderer.draw(self.screen)
        self.card_renderer.draw(self.screen)
        self.mask_renderer.draw(self.screen)
        self.button_renderer.draw(self.screen)
        self.particle_renderer.draw(self.screen)

        # debug purposes
        if SETTINGS_REF.RENDER_BBS:
            self.bb_renderer.draw(self.screen)

        scaled_screen = pygame.transform.scale(
            self.screen, (self.display.get_width(), self.display.get_height())
        )

        self.display.blit(
            scaled_screen, scaled_screen.get_rect(topleft=(0, 0))
        )


_RENDER_PROC_WORLD_DICT: Dict[WorldEnum, RenderingProcessor] = {}
for world in WorldEnum:
    _RENDER_PROC_WORLD_DICT.update({world: RenderingProcessor()})


def RENDER_PROC_REF() -> RenderingProcessor:
    return _RENDER_PROC_WORLD_DICT[WORLD_REF.world]
