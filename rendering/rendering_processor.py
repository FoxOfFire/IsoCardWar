import esper
import pygame

from common import PositionTracker


class ScreenNotFoundException(Exception):
    pass


class RenderingProcessor(esper.Processor):

    def __init__(
        self,
        screen_space_tracker: PositionTracker,
    ) -> None:
        self.window_surf = pygame.display.get_surface()
        if self.window_surf is None:
            raise ScreenNotFoundException()

    def process(self) -> None:
        if self.window_surf is None:
            raise ScreenNotFoundException()
        self.window_surf.fill((200, 200, 200))
