from layer1 import GAME_STATE_REF as STATE_REF
from layer1 import GamePhaseEnum

from .log import logger


def end_phase() -> None:
    assert STATE_REF.game_phase != GamePhaseEnum.END_GAME
    logger.info(f"ending phase: {STATE_REF.game_phase}")

    current_state = STATE_REF.game_phase.value
    last_valid_state = GamePhaseEnum.END_GAME.value - 1

    STATE_REF.game_phase = (
        GamePhaseEnum(current_state + 1)
        if current_state != last_valid_state
        else GamePhaseEnum.DRAW
    )


def end_player_phase(ent: int) -> None:
    STATE_REF.end_player_phase = True
