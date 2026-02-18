from typing import Optional

import esper

from common import ActionArgs

from .enums import WorldEnum


class SceneSwitcherProcessor(esper.Processor):
    _next_tick_world: Optional[WorldEnum]
    _current_world: Optional[WorldEnum]

    def __init__(self) -> None:
        self._next_tick_world = None
        self._current_world = None

    def process(self) -> None:
        if (
            self._next_tick_world is not None
            and esper.current_world != self._next_tick_world.name
        ):
            world = self._next_tick_world.name
            self._current_world = self._next_tick_world
            self._next_tick_world = None
            esper.switch_world(world)

    def switch_world_to(self, world: WorldEnum) -> None:
        self._next_tick_world = world

    def get_world(self) -> WorldEnum:
        if self._current_world is None:
            self._current_world = WorldEnum.GAME

        return self._current_world


def switch_world_action(
    _: ActionArgs, world: Optional[WorldEnum] = None
) -> None:
    if world is None:
        world = SCENE_SWITCH_PROC_REF.get_world()
    SCENE_SWITCH_PROC_REF.switch_world_to(
        WorldEnum((world.value) % len(WorldEnum) + 1)
    )


SCENE_SWITCH_PROC_REF = SceneSwitcherProcessor()
