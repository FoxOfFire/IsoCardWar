from random import randint
from typing import Dict, List, Optional, Tuple, Type

import esper

from common import SETTINGS_REF, Action, BoundingBox, Untracked

from .tile import TerrainEnum, Tile, UnitTypeEnum


class MapData:
    __tracker_tag: Optional[Type] = None
    __sprite: Optional[Type] = None
    __tiles: Dict[Tuple[int, int], int] = {}
    __unit_actions: Dict[UnitTypeEnum | None, List[Action]] = {}

    def set_tracker_tag(self, tag: Type) -> None:
        self.tracker_tag = tag

    def set_sprite(self, sprite: Type) -> None:
        self.sprite = sprite

    def set_actions_for_type(
        self, unit: Optional[UnitTypeEnum], actions: List[Action]
    ) -> None:
        self.__unit_actions.update({unit: actions})

    def get_actions_for_type(
        self, unit: Optional[UnitTypeEnum]
    ) -> List[Action]:
        return self.__unit_actions[unit]

    def make_map(self) -> None:
        assert self.tracker_tag is not None and self.sprite is not None
        w, h = SETTINGS_REF.ISO_MAP_WIDTH, SETTINGS_REF.ISO_MAP_HEIGHT
        rpos = randint(0, w - 1), randint(0, h - 1)
        for i in range(h):
            for j in range(w):
                bb = BoundingBox(i, i + 1, j, j + 1)
                x, y = round(bb.left), round(bb.top)
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
                        unit = UnitTypeEnum(
                            randint(1, len(list(UnitTypeEnum)))
                        )

                tile = Tile(x, y, terrain, unit=unit)

                ent = esper.create_entity(
                    bb, self.sprite(), self.tracker_tag(), tile, Untracked()
                )
                self.__tiles.update({(i, j): ent})

    def ent_at(self, pos: Tuple[int, int]) -> int:
        return self.__tiles[pos]


MAP_DATA_REF = MapData()
