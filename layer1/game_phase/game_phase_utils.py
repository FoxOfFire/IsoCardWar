from layer1 import GAME_STATE_REF, GamePhaseEnum

from .log import logger


def end_phase() -> None:
    assert GAME_STATE_REF.game_phase != GamePhaseEnum.END_GAME
    logger.info(f"ending phase: {GAME_STATE_REF.game_phase}")
    if GAME_STATE_REF.game_phase.value == GamePhaseEnum.END_GAME.value - 1:
        GAME_STATE_REF.game_phase = GamePhaseEnum.DRAW
        return
    GAME_STATE_REF.game_phase = GamePhaseEnum(GAME_STATE_REF.game_phase.value + 1)


def end_player_phase(ent: int) -> None:
    GAME_STATE_REF.end_player_phase = True
