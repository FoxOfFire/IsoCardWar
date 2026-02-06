from typing import Callable, Type

from common import POS_PROC_REF, RUN_DATA_REF, BoundingBox
from layer1 import GAME_STATE_REF


def get_tracked_bb_of_type_str(ty: Type, name: str) -> Callable[[], str]:
    return lambda: f"{name}: {str(POS_PROC_REF.tracked_count_of_type(ty))}"


def get_intersection_count(
    name: str, bb: BoundingBox, ty: Type
) -> Callable[[], str]:
    return lambda: f"{name}x{len(POS_PROC_REF.intersect(bb, ty))}"


def get_fps_str() -> str:
    return f"FPS: {round(RUN_DATA_REF.game_clock.get_fps())}"


def get_game_phase_str() -> str:
    return f"{GAME_STATE_REF.game_phase.name}"
