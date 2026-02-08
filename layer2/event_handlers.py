import pygame

from common import EVENT_PROC_REF

from .scene_switcher import SCENE_SWITCH_PROC_REF
from .ui import SWITCH_SCENE


def handle_world_switch(event: pygame.event.Event) -> None:
    SCENE_SWITCH_PROC_REF.next_tick_world = event.dict["world"]
    # esper.switch_world(event.dict["world"])
    """
    for ent, _ in esper.get_component(UIElementComponent):
        logger.info(ent)
        for comp in esper.components_for_entity(ent):
            logger.info(f"\t{type(comp)}")
    """


def bind_events() -> None:
    EVENT_PROC_REF.bind(SWITCH_SCENE, handle_world_switch)
