from typing import Tuple, Type

import esper

from common import BoundingBox
from layer1.iso_map import make_map, map_obj
from layer2.tags import UIElementComponent
from layer2.ui.ui_events import click_on_tile

from .log import logger


def spawn_iso_elem(
    offset: Tuple[float, float],
    map_size: Tuple[int, int],
    map_scale: Tuple[int, int],
    map_tracker: Type,
    map_sprite: Type,
    ui_tracker: Type,
) -> int:
    map_obj.tracker_tag = map_tracker
    map_obj.sprite = map_sprite
    map_obj.size = map_size

    left = offset[0]
    right = offset[0] + map_size[0] * map_scale[0] + map_size[1] * map_scale[0]
    top = offset[1] - map_size[1] * map_scale[1] / 2 + map_scale[1]
    bottom = offset[1] + map_size[0] * map_scale[1] * 3 / 2 + map_scale[1]
    ui_bb = BoundingBox(left, right, top, bottom)
    logger.info(f"map ui elem created:{ui_bb.points}")

    ent = esper.create_entity(
        ui_bb, ui_tracker(), UIElementComponent(click_func=click_on_tile)
    )
    make_map()
    return ent
