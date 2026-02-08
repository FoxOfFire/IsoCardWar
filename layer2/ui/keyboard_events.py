from typing import Optional

import pygame
from pygame.event import Event

from common import EVENT_PROC_REF, GAME_STATE_REF
from layer1 import (
    DECK_REF,
    OrganizationEnum,
    draw_card,
)


def key_bind_handler(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
            quit_game(None, None)
        elif event.key == pygame.K_q:
            draw_card()
        elif event.key == pygame.K_w:
            GAME_STATE_REF.play_card(None, 0)
        elif event.key == pygame.K_a:
            DECK_REF.set_order(OrganizationEnum.MARKER)
        elif event.key == pygame.K_s:
            DECK_REF.set_order(OrganizationEnum.NAME)
        elif event.key == pygame.K_d:
            DECK_REF.set_order(OrganizationEnum.NONE)


def mouse_handler(event: Event) -> None:
    if event.dict["button"] == 3:
        GAME_STATE_REF.unselect()


def quit_game(_: Optional[int], __: Optional[int]) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def bind_events() -> None:
    EVENT_PROC_REF.bind(pygame.KEYDOWN, key_bind_handler)
    EVENT_PROC_REF.bind(pygame.MOUSEBUTTONUP, mouse_handler)
