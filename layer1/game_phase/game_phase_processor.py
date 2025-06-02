import esper

from common.globals import RUN_DATA_REF
from layer1 import GAME_STATE_REF, GamePhaseEnum

from .game_phase_utils import end_phase
from .log import logger


class GamePhaseProcessor(esper.Processor):
    def __init__(self) -> None:
        logger.info("GamePhaseProcessor init finished")
        self.timer: int = 0

    def _begin_game_phase(self) -> None:
        self.timer += RUN_DATA_REF.delta_time
        if self.timer > 1000:
            self.timer = 0
            end_phase()

    def _draw_phase(self) -> None:
        self.timer += RUN_DATA_REF.delta_time
        if self.timer > 1000:
            self.timer = 0
            end_phase()

    def _player_action_phase(self) -> None:
        if GAME_STATE_REF.end_player_phase:
            GAME_STATE_REF.end_player_phase = False
            self.timer = 0
            end_phase()

    def _end_turn_phase(self) -> None:
        self.timer += RUN_DATA_REF.delta_time
        if self.timer > 1000:
            self.timer = 0
            end_phase()

    def _enemy_action_phase(self) -> None:
        self.timer += RUN_DATA_REF.delta_time
        if self.timer > 1000:
            self.timer = 0
            end_phase()

    def _end_game_phase(self) -> None:
        pass

    def process(self) -> None:
        match GAME_STATE_REF.game_phase:
            case GamePhaseEnum.BEGIN_GAME:
                self._begin_game_phase()
            case GamePhaseEnum.DRAW:
                self._draw_phase()
            case GamePhaseEnum.PLAYER_ACTION:
                self._player_action_phase()
            case GamePhaseEnum.END_OF_TURN:
                self._end_turn_phase()
            case GamePhaseEnum.ENEMY_ACTION:
                self._enemy_action_phase()
            case GamePhaseEnum.END_GAME:
                self._end_game_phase()
            case _:
                RuntimeError("unexpected game phase")
