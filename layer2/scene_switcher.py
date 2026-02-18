from typing import Optional

import esper

from common import STATE_REF, WORLD_REF, ActionArgs, WorldEnum

from .log import logger


class SceneSwitcherProcessor(esper.Processor):
    _next_tick_world: Optional[WorldEnum]

    def __init__(self) -> None:
        self._next_tick_world = None

    def process(self) -> None:
        if (
            self._next_tick_world is not None
            and esper.current_world != self._next_tick_world.name
        ):
            WORLD_REF.world = self._next_tick_world
            self._next_tick_world = None
            STATE_REF.selected_card = None
            STATE_REF.selected_tile = None
            STATE_REF.hovered_ent = None

            esper.switch_world(WORLD_REF.world.name)

    def switch_world_to(self, world: WorldEnum) -> None:
        self._next_tick_world = world


def switch_world_action(
    _: ActionArgs, world: Optional[WorldEnum] = None
) -> None:
    if world is None:
        world = WORLD_REF.world
    sw_to = WorldEnum((world.value) % (len(WorldEnum)) + 1)
    logger.info((world.name, sw_to.name))
    SCENE_SWITCH_PROC_REF.switch_world_to((sw_to))


SCENE_SWITCH_PROC_REF = SceneSwitcherProcessor()
