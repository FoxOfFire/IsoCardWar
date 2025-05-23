from collections.abc import Callable
from typing import List

import esper

from .tile import TerrainEnum, Tile


def change_tile(terrain: TerrainEnum) -> List[Callable[[int, int], None]]:
    effects: List[Callable[[int, int], None]] = []

    def change(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        tile.terrain = terrain

    effects.append(change)
    return effects
