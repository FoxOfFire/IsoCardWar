from common.globals import RUN_DATA_REF
from layer1 import GAME_STATE_REF


def get_fps_str() -> str:
    return f"FPS: {round(RUN_DATA_REF.game_clock.get_fps())}"


def get_game_phase_str() -> str:
    return f"{GAME_STATE_REF.game_phase.name}"
