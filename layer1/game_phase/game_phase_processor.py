from typing import Callable, Dict, List, Optional

import esper

from common import (
    RUN_DATA_REF,
    SETTINGS_REF,
    STATE_REF,
    Action,
    GamePhaseType,
)

from .log import logger


class GamePhaseProcessor(esper.Processor):
    end_phase: Optional[Action]

    def __init__(self) -> None:
        self.wait = SETTINGS_REF.GAME_PHASE_PAUSE
        self.phase_funk_queue: Dict[
            GamePhaseType, Callable[[], List[Action]]
        ] = {}
        self.next_funk_queue: List[Action] = []
        logger.info("GamePhaseProcessor init finished")
        self.end_phase = None

    def _non_player_phase(self) -> None:
        self.wait = max(0, self.wait - RUN_DATA_REF.delta_time)
        if self.wait > 0:
            return

        phase: GamePhaseType = STATE_REF.game_phase

        logger.info(f"{esper.current_world, len(self.next_funk_queue)}")
        if len(self.next_funk_queue) > 0:
            logger.info(self.wait)
            while self.wait == 0 and len(self.next_funk_queue) > 0:
                self.next_funk_queue.pop()(STATE_REF.selected_tile)
            return
        if phase == GamePhaseType.END_GAME:
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
        if phase == GamePhaseType.PLAYER_ACTION:
            self._player_action_phase()
        else:
            self._non_player_phase()

    def add_game_phase(
        self, phase: GamePhaseType, func_list: Callable[[], List[Action]]
    ) -> None:
        logger.info("adding game phase:" + str(phase.name))
        self.phase_funk_queue.update({phase: func_list})

    def set_end_phase(self, fun: Action) -> None:
        logger.info("set end phase")
        self.end_phase = fun


GAME_PHASE_PROC_REF = GamePhaseProcessor()
