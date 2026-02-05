import pygame
from pygame.event import Event

from common import EventProcessor
from layer1 import unselect
from layer1.cards import DECK_REF, OrganizationEnum, discard_card, draw_card


def key_bind_handler(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
            quit_game(-1)
        elif event.key == pygame.K_q:
            draw_card()
        elif event.key == pygame.K_w:
            discard_card(0)
        elif event.key == pygame.K_a:
            DECK_REF.set_order(OrganizationEnum.MARKER)
        elif event.key == pygame.K_s:
            DECK_REF.set_order(OrganizationEnum.NAME)
        elif event.key == pygame.K_d:
            DECK_REF.set_order(OrganizationEnum.NONE)


def mouse_handler(event: Event) -> None:
    if event.dict["button"] == 3:
        unselect()


def quit_game(ent: int) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def bind_events(event_processor: EventProcessor) -> None:
    event_processor.bind(pygame.KEYDOWN, key_bind_handler)
    event_processor.bind(pygame.MOUSEBUTTONUP, mouse_handler)
