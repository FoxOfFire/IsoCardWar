from collections.abc import Callable
from typing import List

import esper

from .log import logger
from .tile import SelectionTypeEnum, TerrainEnum, Tile, UnitTypeEnum


def change_tile_to(terrain: TerrainEnum) -> List[Callable[[int, int], None]]:
    effects: List[Callable[[int, int], None]] = []

    def change(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        tile.terrain = terrain

    effects.append(change)
    return effects


def change_tile() -> List[Callable[[int, int], None]]:
    effects: List[Callable[[int, int], None]] = []

    def rotate(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        logger.info(tile.terrain)
        tile.terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)

    effects.append(rotate)

    return effects


def change_unit() -> List[Callable[[int, int], None]]:
    effects: List[Callable[[int, int], None]] = []

    def rotate(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        logger.info(tile.terrain)
        n = tile.unit.value if tile.unit is not None else 0
        n = (n + 1) % (len(list(UnitTypeEnum)) + 1)
        unit = None if n == 0 else UnitTypeEnum(n)
        tile.unit = unit

    effects.append(rotate)

    return effects


def change_selection() -> List[Callable[[int, int], None]]:
    effects: List[Callable[[int, int], None]] = []

    def rotate(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        logger.info(tile.terrain)
        n = tile.selection.value if tile.selection is not None else 0
        n = (n + 1) % (len(list(SelectionTypeEnum)) + 1)
        selection = None if n == 0 else SelectionTypeEnum(n)
        tile.selection = selection

    effects.append(rotate)

    return effects
