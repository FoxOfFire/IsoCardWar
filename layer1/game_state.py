from collections.abc import Callable
from typing import Dict, Optional

import esper

from .game_state_utils import PriceEnum


class GameState:
    def __init__(self) -> None:
        self.resources: Dict[PriceEnum, int]
        self.play_card: Optional[Callable[[int], None]]
        self.get_selected: Optional[Callable[[], int]]
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None


game_state_obj = GameState()


# cards
def set_play_card(func: Callable[[int], None]) -> None:
    game_state_obj.play_card = func


def play_card(target: int) -> None:
    if game_state_obj.play_card is None:
        return
    game_state_obj.play_card(target)


def remove_hover(_: int) -> None:
    game_state_obj.selecting = None


def unselect() -> None:
    game_state_obj.selected = None


def select(ent: int) -> None:
    if not esper.entity_exists(ent):
        return
    game_state_obj.selected = ent


def hover(ent: int) -> None:
    if not esper.entity_exists(ent):
        return
    game_state_obj.selecting = ent
