import pygame
from pygame.event import Event

from common import EventProcessor
from layer1 import unselect
<<<<<<< HEAD
from layer1.cards import DECK_REF, OrganizationEnum, draw_card
=======
from layer1.cards import OrganizationEnum, deck_obj, draw_card
>>>>>>> master


def key_bind_handler(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
<<<<<<< HEAD
            quit_game(-1)
=======
            pygame.event.post(pygame.event.Event(pygame.QUIT))
>>>>>>> master
        elif event.key == pygame.K_q:
            draw_card()
        elif event.key == pygame.K_a:
            DECK_REF.set_order(OrganizationEnum.MARKER)
        elif event.key == pygame.K_s:
            DECK_REF.set_order(OrganizationEnum.NAME)
        elif event.key == pygame.K_d:
            DECK_REF.set_order(OrganizationEnum.NONE)


def mouse_handler(event: Event) -> None:
    if event.dict["button"] == 3:
        unselect()
<<<<<<< HEAD


def quit_game(ent: int) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))
=======
>>>>>>> master


def bind_events(event_processor: EventProcessor) -> None:
    event_processor.bind(pygame.KEYDOWN, key_bind_handler)
    event_processor.bind(pygame.MOUSEBUTTONUP, mouse_handler)
