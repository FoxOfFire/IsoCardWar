from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1 import play_card
from layer1.iso_map import map_obj
from layer2.tags import GameCameraTag

from .log import logger

SWITCH_SCENE = pygame.event.custom_type()


class SelectionException(Exception):
    pass


@dataclass
class UIEventInfo:
    iso_pos_track: Optional[PositionTracker] = None
    iso_click_event: Optional[Callable[..., None]] = None


ui_event_obj = UIEventInfo()
logger.info("ui_event_obj created")


# /\       T~~T
# /  \ ---\ |  |
# \  / ---/ |  |
# \/       L__J
# https://www.desmos.com/calculator/by4alm9as1
def _get_transformed_mouse_pos(bb: BoundingBox) -> Tuple[float, float]:
    cam_bb = esper.component_for_entity(
        esper.get_component(GameCameraTag)[0][0], BoundingBox
    )

    display_rect = pygame.display.get_surface().get_rect()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    map_width, map_height = map_obj.size

    x = (mouse_x * cam_bb.width / display_rect.width - bb.left) / bb.width
    y = (mouse_y * cam_bb.height / display_rect.height - bb.top) / bb.height

    calc_y = (x - y + 1 / 2) * map_width
    calc_x = (y + x - 1 / 2) * map_height

    return calc_x, calc_y


def click_on_tile(ent: int) -> None:
    bb = esper.component_for_entity(ent, BoundingBox)
    trans_mouse_pos = _get_transformed_mouse_pos(bb)
    mouse_bb = BoundingBox(
        trans_mouse_pos[0], trans_mouse_pos[0], trans_mouse_pos[1], trans_mouse_pos[1]
    )
    if ui_event_obj.iso_pos_track is None:
        raise RuntimeError("ui_event_obj iso_pos_track field missing")

    for intersect in ui_event_obj.iso_pos_track.intersect(mouse_bb):
        if (
            esper.component_for_entity(intersect, BoundingBox).points
            == esper.component_for_entity(
                ui_event_obj.iso_pos_track.plain, BoundingBox
            ).points
        ):
            continue
        play_card(intersect)
