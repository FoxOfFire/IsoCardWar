from typing import List

from common.types import ButtonFunc

from .cards import draw_card


def draw_cards(count: int) -> List[ButtonFunc]:
    def _draw(ent: int, target: int) -> None:
        draw_card()

    effects: List[ButtonFunc] = []
    for _ in range(count):
        effects.append(_draw)

    return effects
