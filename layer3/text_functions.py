from typing import Callable

import esper

from common import POS_PROC_REF, RUN_DATA_REF, STATE_REF, PriceEnum
from layer1 import Particle


def get_tracked_bb_of_type_str() -> str:
    return f"tracked: {str(POS_PROC_REF().tracked_count())}"


def get_resource_amount(resource: PriceEnum) -> str:
    return f"{STATE_REF.resources[resource]}"


def get_game_world_str() -> str:
    return f"World: {esper.current_world}"


def get_particle_count_str() -> str:
    return f"Particle Count: {len(esper.get_component(Particle))}"


def get_fps_str() -> str:
    return f"FPS: {round(RUN_DATA_REF.game_clock.get_fps())}"


def get_game_phase_str() -> str:
    return f"{STATE_REF.game_phase.name}"


def text_funcify(text: str | Callable[[], str]) -> Callable[[], str]:
    if callable(text):
        return text
    else:
        return lambda: text
