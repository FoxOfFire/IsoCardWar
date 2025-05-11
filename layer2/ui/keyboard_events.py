import pygame
from pygame.event import Event

from common import EventProcessor
from layer1.cards import deck_obj, draw_card, play_card


def quit_via_kb(event: Event) -> None:
    if event.key is not None:
        if event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif event.key == pygame.K_e:
            draw_card()
        elif event.key == pygame.K_q:
            if len(deck_obj.hand) > 0:
                play_card(deck_obj.hand[len(deck_obj.hand) - 1])


def bind_events(event_processor: EventProcessor) -> None:
    event_processor.bind(pygame.KEYDOWN, quit_via_kb)
