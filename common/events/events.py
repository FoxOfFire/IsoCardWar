from typing import Callable, Dict

import esper
import pygame

from common.worlds import WORLD_REF, WorldEnum

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


_EVENT_PROC_WORLD_DICT: Dict[WorldEnum, EventProcessor] = {}
for world in WorldEnum:
    _EVENT_PROC_WORLD_DICT.update({world: EventProcessor()})


def EVENT_PROC_REF() -> EventProcessor:
    return _EVENT_PROC_WORLD_DICT[WORLD_REF.world]
