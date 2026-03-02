from common import STATE_REF, Action, ActionDecor, ActionEnt, GamePhaseType

from .game_phase_processor import GAME_PHASE_PROC_REF
from .log import logger


def get_wait_ms_action(ms: int) -> Action:
    @ActionDecor
    def action(_: ActionEnt) -> bool:
        logger.info(f"wait for {ms}ms")
        GAME_PHASE_PROC_REF.wait += ms
        return True

    return action


@ActionDecor
def end_phase(_: ActionEnt = None) -> bool:
    if STATE_REF.game_phase == GamePhaseType.END_GAME:
        return False
    logger.info(f"ending phase: {STATE_REF.game_phase.name}")

    current_state = STATE_REF.game_phase.value
    last_valid_state = GamePhaseType.END_GAME.value - 1

    STATE_REF.game_phase = (
        GamePhaseType(current_state + 1)
        if current_state != last_valid_state
        else GamePhaseType(GamePhaseType.BEGIN_GAME.value + 1)
    )
    GAME_PHASE_PROC_REF.next_funk_queue = GAME_PHASE_PROC_REF.phase_funk_queue[
        STATE_REF.game_phase
    ]()
    return True
