from common import (
    GAME_STATE_REF,
    ActionArgs,
    GamePhaseEnum,
)

from .log import logger


def end_phase(_: ActionArgs = None) -> None:

    assert GAME_STATE_REF.game_phase != GamePhaseEnum.END_GAME
    logger.info(f"ending phase: {GAME_STATE_REF.game_phase}")

    current_state = GAME_STATE_REF.game_phase.value
    last_valid_state = GamePhaseEnum.END_GAME.value - 1

    GAME_STATE_REF.game_phase = (
        GamePhaseEnum(current_state + 1)
        if current_state != last_valid_state
        else GamePhaseEnum.DRAW
    )
