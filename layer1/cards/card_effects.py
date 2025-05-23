from collections.abc import Callable
from typing import List

from .cards import draw_card


def draw_cards(count: int) -> List[Callable[[int, int], None]]:
    def _draw(ent: int, target: int) -> None:
        draw_card()

    effects: List[Callable[[int, int], None]] = []
    for _ in range(count):
        effects.append(_draw)

    return effects
