from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Iterable, Tuple, Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from common.constants import (
    ISO_POS_OFFSET_X,
    ISO_POS_OFFSET_Y,
    ISO_TILE_OFFSET_X,
    ISO_TILE_OFFSET_Y,
    ISO_TILE_SELECT_OFFSET,
)
from layer1 import MarkerEnum, game_state_obj
from layer1.cards import Card
from layer1.iso_map import SelectionTypeEnum, Tile

from .log import logger
from .rendering_asset_loader import SELECTION_SURFS, TILE_TYPE_SURFS, UNIT_TYPE_SURFS


@dataclass
class IsoSprite:
    pass


class IsoRenderer:
    def __init__(self, pos_track: PositionTracker, tag: Type, /) -> None:
        super().__init__()
        self.pos_track = pos_track
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )
        logger.info("iso renderer init finished")

    class _DrawType(Enum):
        TILE = auto()
        UNIT = auto()
        SELECTION = auto()

    def _draw_type(
        self,
        screen: pygame.Surface,
        surfs: Dict[Enum, pygame.Surface],
        ent_list: Iterable[int],
        draw_type: _DrawType,
        /,
        *,
        offset: Tuple[float, float] = (0, 0),
    ) -> None:
        delta_x, delta_y = offset
        for ent in ent_list:
            if not esper.has_component(ent, IsoSprite):
                continue
            tile = esper.component_for_entity(ent, Tile)
            x = delta_x + ISO_POS_OFFSET_X + (tile.x + tile.y) * ISO_TILE_OFFSET_X
            y = delta_y + ISO_POS_OFFSET_Y + (tile.x - tile.y) * ISO_TILE_OFFSET_Y
            if ent == game_state_obj.selecting:
                y += ISO_TILE_SELECT_OFFSET
            match draw_type:
                case self._DrawType.TILE:
                    screen.blit(surfs[tile.terrain], (x, y))

                case self._DrawType.UNIT:
                    if tile.unit is not None:
                        screen.blit(surfs[tile.unit], (x, y))

                case self._DrawType.SELECTION:
                    if ent != game_state_obj.selecting:
                        continue
                    if game_state_obj.selected is None:
                        continue
                    card = esper.try_component(game_state_obj.selected, Card)
                    if card is None:
                        continue
                    match card.marker:
                        case MarkerEnum.BUILDING:
                            screen.blit(surfs[SelectionTypeEnum.BLUE], (x, y))
                        case MarkerEnum.ACTION:
                            screen.blit(surfs[SelectionTypeEnum.RED], (x, y))
                        case MarkerEnum.UNIT:
                            screen.blit(surfs[SelectionTypeEnum.GREEN], (x, y))
                        case MarkerEnum.UNIQUE:
                            pass
                        case _:
                            raise RuntimeError("unexpected card marker in selection")

                case _:
                    raise RuntimeError("unexpected type while drawing iso_tiles")

    def draw(self, screen: pygame.Surface) -> None:
        def sort_by_bottom(ent: int) -> int:
            tile = esper.try_component(ent, Tile)
            if tile is None:
                return -1
            return tile.x - tile.y

        ent_list = sorted(
            self.pos_track.intersect(self.bb),
            key=lambda ent: sort_by_bottom(ent),
        )
        self._draw_type(screen, TILE_TYPE_SURFS, ent_list, self._DrawType.TILE)
        self._draw_type(
            screen,
            SELECTION_SURFS,
            ent_list,
            self._DrawType.SELECTION,
            offset=(0, -ISO_TILE_OFFSET_Y * 2),
        )
        self._draw_type(
            screen,
            UNIT_TYPE_SURFS,
            ent_list,
            self._DrawType.UNIT,
            offset=(0, -ISO_TILE_OFFSET_Y * 2),
        )
