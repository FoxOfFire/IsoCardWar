from typing import Type

import esper

from common import (
    POS_PROC_REF,
    RUN_DATA_REF,
    STATE_REF,
    BoundingBox,
    PriceEnum,
    TextFuncDecor,
)


def get_tracked_bb_of_type_str(ty: Type, name: str) -> str:
    return f"{name}: {str(POS_PROC_REF().tracked_count_of_type(ty))}"


def get_intersection_count(name: str, bb: BoundingBox, ty: Type) -> str:
    return f"{name}x{len(POS_PROC_REF().intersect(bb, ty))}"


def get_resource_amount(resource: PriceEnum) -> str:
    return f"{STATE_REF.resources[resource]}"


@TextFuncDecor
def get_game_world_str() -> str:
    return f"World: {esper.current_world}"


@TextFuncDecor
def get_fps_str() -> str:
    return f"FPS: {round(RUN_DATA_REF.game_clock.get_fps())}"


@TextFuncDecor
def get_game_phase_str() -> str:
    return f"{STATE_REF.game_phase.name}"
