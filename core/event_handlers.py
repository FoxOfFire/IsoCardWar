import functools

import pygame

from common import EventProcessor
from ui import SWITCH_SCENE

from .scene_switcher import SceneSwitcher


def handle_world_switch(
    event: pygame.event.Event, scene_switcher: SceneSwitcher
) -> None:
    scene_switcher.next_tick_world = event.dict["world"]
    # esper.switch_world(event.dict["world"])
    """
    for ent, _ in esper.get_component(UIElementComponent):
        logger.info(ent)
        for comp in esper.components_for_entity(ent):
            logger.info(f"\t{type(comp)}")
    """


def bind_events(event_processor: EventProcessor, scene_switcher: SceneSwitcher) -> None:
    event_processor.bind(
        SWITCH_SCENE,
        functools.partial(handle_world_switch, scene_switcher=scene_switcher),
    )
