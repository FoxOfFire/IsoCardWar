from typing import Optional

import esper

from common import (
    POS_PROC_REF,
    STATE_REF,
    WORLD_REF,
    Action,
    ActionArgs,
    TempObjectTag,
    WorldEnum,
)


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
            STATE_REF.hovered_ent = None

            for ent, _ in esper.get_component(TempObjectTag):
                POS_PROC_REF().untrack(ent)
                esper.delete_entity(ent)

            esper.switch_world(WORLD_REF.world.name)

    def switch_world_to(self, world: WorldEnum) -> None:
        self._next_tick_world = world


def get_switch_world_action(world: WorldEnum) -> Action:
    def sw_a(_: ActionArgs = None) -> None:
        SCENE_SWITCH_PROC_REF.switch_world_to((world))

    fn = sw_a
    return fn


SCENE_SWITCH_PROC_REF = SceneSwitcherProcessor()
