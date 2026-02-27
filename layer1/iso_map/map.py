from random import randint
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

import esper
import pygame

from common import SETTINGS_REF, Action, BoundingBox, Untracked

from .tile import TerrainEnum, Tile, UnitTypeEnum


class MapData:
    _sprite: Optional[Type] = None
    _particle_generator: Optional[Type] = None
    _tiles: Dict[Tuple[int, int], int] = {}
    _ents: Dict[int, Tuple[int, int]] = {}
    _unit_actions: Dict[UnitTypeEnum | None, List[Action]] = {}
    _unit_telegraphs: Dict[UnitTypeEnum | None, List[Action]] = {}

    def set_particle_generator(self, tag: Type) -> None:
        self._particle_generator = tag

    def set_sprite(self, sprite: Type) -> None:
        self._sprite = sprite

    def set_actions_for_type(
        self, actions: Dict[Optional[UnitTypeEnum], List[Action]]
    ) -> None:
        self._unit_actions.update(actions)

    def get_actions_for_type(
        self, unit: Optional[UnitTypeEnum]
    ) -> List[Action]:
        return self._unit_actions[unit]

    def set_telegraph_for_type(
        self, telegraphs: Dict[Optional[UnitTypeEnum], List[Action]]
    ) -> None:
        self._unit_telegraphs.update(telegraphs)

    def get_telegraphs_for_type(
        self, unit: Optional[UnitTypeEnum]
    ) -> List[Action]:
        return self._unit_telegraphs[unit]

    def _spawn_iso_item_at(
        self,
        i: int,
        j: int,
        rpos: Tuple[int, int],
        get_ui_component: Callable[[], Any],
    ) -> None:
        terrain = TerrainEnum(randint(1, len(list(TerrainEnum))))
        unit: Optional[UnitTypeEnum] = None

        if (j, i) == rpos:
            terrain = TerrainEnum.GRASS
            unit = UnitTypeEnum.WITCH
        elif (
            randint(0, 2) == 0
            and terrain != TerrainEnum.WATER
            and terrain != TerrainEnum.EMPTY
        ):
            while unit == UnitTypeEnum.WITCH or unit is None:
                unit = UnitTypeEnum(randint(1, len(list(UnitTypeEnum))))

        tile = Tile(i, j, terrain, unit=unit)

        sprite_offset = (
            tile.x_offset,
            tile.y_offset + SETTINGS_REF.ISO_TILE_OFFSET_Y * 2,
        )
        sprite_size = (
            SETTINGS_REF.ISO_TILE_OFFSET_X * 2,
            SETTINGS_REF.ISO_TILE_OFFSET_Y * 2,
        )
        bb = BoundingBox(
            tile.x_offset,
            tile.x_offset + SETTINGS_REF.ISO_TILE_OFFSET_X * 2,
            tile.y_offset + SETTINGS_REF.ISO_TILE_OFFSET_Y * 2,
            tile.y_offset + SETTINGS_REF.ISO_TILE_OFFSET_Y * 4,
        )
        assert (
            self._sprite is not None and self._particle_generator is not None
        )
        ent = esper.create_entity(
            bb,
            get_ui_component(),
            self._sprite(pygame.Rect(sprite_offset, sprite_size)),
            tile,
            Untracked(),
            self._particle_generator(),
        )
        self._tiles.update({(i, j): ent})
        self._ents.update({ent: (i, j)})

    def make_map(self, get_ui_component: Callable[[], Any]) -> None:
        w, h = SETTINGS_REF.ISO_MAP_WIDTH, SETTINGS_REF.ISO_MAP_HEIGHT
        rpos = randint(0, w - 1), randint(0, h - 1)
        for i in range(h):
            for j in range(w):
                self._spawn_iso_item_at(i, j, rpos, get_ui_component)

    def ent_at(self, pos: Tuple[int, int]) -> int:
        return self._tiles[pos]

    def pos_at(self, ent: int) -> Tuple[int, int]:
        return self._ents[ent]


MAP_DATA_REF = MapData()
