from common import (
    STATE_REF,
    ActionArgs,
    GamePhaseEnum,
)

from .game_phase_processor import GAME_PHASE_PROC_REF
from .log import logger


def end_phase(_: ActionArgs = None) -> None:

    assert STATE_REF.game_phase != GamePhaseEnum.END_GAME
    logger.info(f"ending phase: {STATE_REF.game_phase}")

    current_state = STATE_REF.game_phase.value
    last_valid_state = GamePhaseEnum.END_GAME.value - 1

    STATE_REF.game_phase = (
        GamePhaseEnum(current_state + 1)
        if current_state != last_valid_state
        else GamePhaseEnum.DRAW
    )
    GAME_PHASE_PROC_REF.next_funk_queue = GAME_PHASE_PROC_REF.phase_funk_queue[
        STATE_REF.game_phase
    ].copy()
