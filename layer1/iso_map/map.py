from dataclasses import dataclass
from typing import Optional, Tuple, Type

import esper
import pygame

from common import BoundingBox

from .log import logger


@dataclass
class Tile:
    x: int
    y: int
    col: pygame.Color


class Map:
    def __init__(self) -> None:
        self.tracker_tag: Optional[Type] = None
        self.sprite: Optional[Type] = None
        self.size: Tuple[int, int] = (-1, -1)


map_obj = Map()


def make_map() -> None:
    if (
        map_obj.tracker_tag is None
        or map_obj.sprite is None
        or map_obj.size == (-1, -1)
    ):
        raise RuntimeError(
            "failed to fetch map data of tracker:"
            + f"{map_obj.tracker_tag}, sprite:{map_obj.sprite} "
            + f"or size:{map_obj.size}"
        )
    w, h = map_obj.size
    tracker = map_obj.tracker_tag
    sprite = map_obj.sprite
    for i in range(h):
        bbs = [
            BoundingBox(i % w, i % w + 1, i, i + 1),
            BoundingBox(w - i % w - 1, w - i % w, i, i + 1),
        ]
        for j in range(len(bbs)):
            esper.create_entity(
                bbs[j],
                sprite(),
                tracker(),
                Tile(
                    round(bbs[j].left),
                    round(bbs[j].top),
                    pygame.Color(i * 30, j * 200, 0),
                ),
            )
