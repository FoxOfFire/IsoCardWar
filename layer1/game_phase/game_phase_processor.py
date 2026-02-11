from typing import Dict, List, Optional

import esper

from common import (
    RUN_DATA_REF,
    SETTINGS_REF,
    STATE_REF,
    Action,
    GamePhaseEnum,
)

from .log import logger


class GamePhaseProcessor(esper.Processor):
    end_phase: Optional[Action]

    def __init__(self) -> None:
        self.wait = SETTINGS_REF.GAME_PHASE_PAUSE
        self.phase_funk_queue: Dict[GamePhaseEnum, List[Action]] = {}
        self.next_funk_queue: List[Action] = []
        logger.info("GamePhaseProcessor init finished")
        self.end_phase = None

    def _non_player_phase(self) -> None:
        self.wait = max(0, self.wait - RUN_DATA_REF.delta_time)
        if self.wait > 0:
            return
        self.wait = SETTINGS_REF.GAME_PHASE_PAUSE

        phase: GamePhaseEnum = STATE_REF.game_phase

        if len(self.next_funk_queue) > 0:
            self.next_funk_queue.pop()(None)
            return
        if phase == GamePhaseEnum.END_GAME:
            return
        assert self.end_phase is not None
        self.end_phase(None)

    def _player_action_phase(self) -> None:
        if STATE_REF.end_player_phase:
            STATE_REF.end_player_phase = False
            self.timer = 0
            assert self.end_phase is not None
            self.end_phase(None)

    def process(self) -> None:
        phase = STATE_REF.game_phase
        if phase == GamePhaseEnum.PLAYER_ACTION:
            self._player_action_phase()
        else:
            self._non_player_phase()

    def add_game_phase(
        self, phase: GamePhaseEnum, /, *, func_list: Optional[List[Action]]
    ) -> None:
        logger.info("adding game phase:" + str(phase))
        if func_list is None:
            func_list = []
        self.phase_funk_queue.update({phase: func_list})

    def set_end_phase(self, fun: Action) -> None:
        logger.info("set end phase")
        self.end_phase = fun


GAME_PHASE_PROC_REF = GamePhaseProcessor()
