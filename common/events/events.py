from typing import Callable

import esper
import pygame

EventHandler = Callable[[pygame.event.Event], None]


class EventProcessor(esper.Processor):
    __bound_events: dict[int, list[EventHandler]]

    def __init__(self) -> None:
        self.__bound_events = dict()

    def bind(self, event_type: int, handler: EventHandler) -> None:
        pygame.event.set_allowed(event_type)
        handlers = self.__bound_events.get(event_type, [])
        handlers.append(handler)
        self.__bound_events[event_type] = handlers

    def process(self) -> None:
        for event in pygame.event.get():
            for handler in self.__bound_events.get(event.type, []):
                handler(event)
