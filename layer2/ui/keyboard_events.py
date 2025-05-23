import pygame
from pygame.event import Event

from common import EventProcessor
from layer1.cards import OrganizationEnum, deck_obj, draw_card, unselect_card


def quit_via_kb(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif event.key == pygame.K_e:
            draw_card()
        elif event.key == pygame.K_w:
            unselect_card()
        elif event.key == pygame.K_a:
            deck_obj.set_order(OrganizationEnum.MARKER)
        elif event.key == pygame.K_s:
            deck_obj.set_order(OrganizationEnum.NAME)


def bind_events(event_processor: EventProcessor) -> None:
    event_processor.bind(pygame.KEYDOWN, quit_via_kb)
