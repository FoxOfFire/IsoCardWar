from random import randint
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

import esper
import pygame
from perlin_noise import PerlinNoise

from common import SETTINGS_REF, Action, BoundingBox, Untracked

from .tile import TerrainEnum, Tile, UnitTypeEnum


class MapData:
    _sprite: Optional[Type] = None
    _particle_generator: Optional[Type] = None
    _tiles: Dict[Tuple[int, int], int] = {}
    _ents: Dict[int, Tuple[int, int]] = {}
    _unit_actions: Dict[UnitTypeEnum | None, List[Action]] = {}
    _unit_telegraphs: Dict[UnitTypeEnum | None, List[Action]] = {}
    _perlin_noise: List[List[float]] = []

    def _generate_noise(self) -> None:
        seed = SETTINGS_REF.ISO_MAP_SEED
        x = SETTINGS_REF.ISO_MAP_WIDTH
        y = SETTINGS_REF.ISO_MAP_HEIGHT
        scale = 0.2

        noise1 = PerlinNoise(octaves=9, seed=seed)
        noise2 = PerlinNoise(octaves=9, seed=seed)
        noise3 = PerlinNoise(octaves=9, seed=seed)

        self._perlin_noise: List[List[float]] = []
        for i in range(x):
            row = []
            for j in range(y):
                noise_val = noise1([i / (x / scale), j / (y / scale)])
                noise_val += 0.5 * noise2([i / (x / scale), j / (y / scale)])
                noise_val += 0.25 * noise3([i / (x / scale), j / (y / scale)])

                noise_val = (noise_val + 1) / 2
                row.append(noise_val)
            self._perlin_noise.append(row)
        print(self._perlin_noise)

    def __init__(self) -> None:
        self._generate_noise()

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
        noise_val = self._perlin_noise[i][j]
        terrain = TerrainEnum(1)
        for k in range(len(list(TerrainEnum))):
            if noise_val < SETTINGS_REF.ISO_NOISE_THRESHOLDS[k]:
                terrain = TerrainEnum(k + 1)
                break
        unit: Optional[UnitTypeEnum] = None

        if (j, i) == rpos:
            terrain = TerrainEnum.GRASS
            unit = UnitTypeEnum.WITCH
        elif (
            randint(0, SETTINGS_REF.ISO_MAP_HEIGHT // 2) == 0
            and terrain != TerrainEnum.WATER
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
