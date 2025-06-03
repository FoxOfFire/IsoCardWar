from collections.abc import Callable
from typing import Dict, List

import esper

from layer1 import GAME_STATE_REF, GamePhaseEnum

from .game_phase_utils import end_phase
from .log import logger


class GamePhaseProcessor(esper.Processor):
    def __init__(
        self, phase_func_dict: Dict[GamePhaseEnum, List[Callable[[], None]]]
    ) -> None:
        logger.info("GamePhaseProcessor init finished")
        self.phase_func_dict = phase_func_dict

    def _non_player_phase(self) -> None:
        phase: GamePhaseEnum = GAME_STATE_REF.game_phase

        for func in self.phase_func_dict[phase]:
            func()
        if phase == GamePhaseEnum.END_GAME:
            return
        end_phase()

    def _player_action_phase(self) -> None:
        if GAME_STATE_REF.end_player_phase:
            GAME_STATE_REF.end_player_phase = False
            self.timer = 0
            end_phase()

    def process(self) -> None:
        phase = GAME_STATE_REF.game_phase
        if phase == GamePhaseEnum.PLAYER_ACTION:
            self._player_action_phase()
        else:
            self._non_player_phase()
