import pygame
from pygame.event import Event

from common import EVENT_PROC_REF, play_card, select
from layer1 import DECK_REF, OrganizationEnum, draw_card, sort_hand

from .ui_actions import quit_game


def key_bind_handler(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
            quit_game()
        elif event.key == pygame.K_q:
            draw_card()
        elif event.key == pygame.K_w:
            play_card(None)
        elif event.key == pygame.K_a:
            DECK_REF.set_order(OrganizationEnum.MARKER)
            sort_hand()
        elif event.key == pygame.K_s:
            DECK_REF.set_order(OrganizationEnum.NAME)
            sort_hand()
        elif event.key == pygame.K_d:
            DECK_REF.set_order(OrganizationEnum.NONE)
            sort_hand()


def mouse_handler(event: Event) -> None:
    if event.dict["button"] == 3:
        select(None)


def bind_events() -> None:
    EVENT_PROC_REF.bind(pygame.KEYDOWN, key_bind_handler)
    EVENT_PROC_REF.bind(pygame.MOUSEBUTTONUP, mouse_handler)
