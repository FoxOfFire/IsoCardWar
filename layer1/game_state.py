from collections.abc import Callable
from typing import Dict, Optional

from .game_state_utils import PriceEnum


class GameState:
    def __init__(self) -> None:
        self.selection: int = -1
        self.resources: Dict[PriceEnum, int]
        self.play_card: Optional[Callable[[int], None]]
        self.get_selected: Optional[Callable[[], int]]


game_state_obj = GameState()


# cards
def set_play_card(func: Callable[[int], None]) -> None:
    game_state_obj.play_card = func


def play_card(target: int) -> None:
    if game_state_obj.play_card is None:
        return
    game_state_obj.play_card(target)


def set_select_obj(ent: int) -> None:
    game_state_obj.selection = ent


def get_select_obj() -> int:
    return game_state_obj.selection


def use_selection_on_tile(ent: int) -> None:
    if game_state_obj.selection is None:
        return
