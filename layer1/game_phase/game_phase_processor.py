from typing import Dict, List, Optional

import esper

from common import GAME_PHASE_PAUSE, RUN_DATA_REF, Action
from layer1.game_state import GAME_STATE_REF, GamePhaseEnum

from .log import logger


class GamePhaseProcessor(esper.Processor):
    def __init__(self) -> None:
        self.wait = GAME_PHASE_PAUSE
        self.phase_funk_queue: Dict[GamePhaseEnum, List[Action]] = {}
        logger.info("GamePhaseProcessor init finished")

    def _non_player_phase(self) -> None:
        self.wait = max(0, self.wait - RUN_DATA_REF.delta_time)
        if self.wait > 0:
            return
        self.wait = GAME_PHASE_PAUSE

        phase: GamePhaseEnum = GAME_STATE_REF.game_phase

        for func in self.phase_funk_queue[phase]:
            func()
        if phase == GamePhaseEnum.END_GAME:
            return
        self.end_phase()

    def _player_action_phase(self) -> None:
        if GAME_STATE_REF.end_player_phase:
            GAME_STATE_REF.end_player_phase = False
            self.timer = 0
            self.end_phase()

    def process(self) -> None:
        phase = GAME_STATE_REF.game_phase
        if phase == GamePhaseEnum.PLAYER_ACTION:
            self._player_action_phase()
        else:
            self._non_player_phase()

    def end_phase(self) -> None:

        assert GAME_STATE_REF.game_phase != GamePhaseEnum.END_GAME
        logger.info(f"ending phase: {GAME_STATE_REF.game_phase}")

        current_state = GAME_STATE_REF.game_phase.value
        last_valid_state = GamePhaseEnum.END_GAME.value - 1

        GAME_STATE_REF.game_phase = (
            GamePhaseEnum(current_state + 1)
            if current_state != last_valid_state
            else GamePhaseEnum.DRAW
        )

    def add_game_phase(
        self, phase: GamePhaseEnum, /, *, func_list: Optional[List[Action]]
    ) -> None:
        if func_list is None:
            func_list = []
        self.phase_funk_queue.update({phase: func_list})


GAME_PHASE_PROC_REF = GamePhaseProcessor()
