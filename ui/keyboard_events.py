import pygame
from pygame.event import Event

from common import EventProcessor


def quit_via_kb(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))


def bind_events(event_processor: EventProcessor) -> None:
    event_processor.bind(pygame.KEYDOWN, quit_via_kb)
