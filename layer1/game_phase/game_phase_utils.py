from layer1.game_state import GAME_STATE_REF, GamePhaseEnum

from .log import logger


def end_phase() -> None:

    assert GAME_STATE_REF.game_phase != GamePhaseEnum.END_GAME
    logger.info(f"ending phase: {GAME_STATE_REF.game_phase}")

    current_state = GAME_STATE_REF.game_phase.value
    last_valid_state = GamePhaseEnum.END_GAME.value - 1

    GAME_STATE_REF.game_phase = (
        GamePhaseEnum(current_state + 1)
        if current_state != last_valid_state
        else GamePhaseEnum.DRAW
    )


def end_player_phase(ent: int) -> None:
    GAME_STATE_REF.end_player_phase = True
