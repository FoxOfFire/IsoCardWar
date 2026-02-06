from typing import List

from common import EntityFunc

from .cards import draw_card


def draw_cards(count: int) -> List[EntityFunc]:
    def _draw(ent: int, target: int) -> None:
        draw_card()

    effects: List[EntityFunc] = []
    for _ in range(count):
        effects.append(_draw)

    return effects
