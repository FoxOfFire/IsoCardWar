from dataclasses import dataclass
from typing import Optional, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1 import hover, play_card, remove_hover
from layer1.iso_map import map_obj
from layer2.tags import GameCameraTag

from .log import logger

SWITCH_SCENE = pygame.event.custom_type()


@dataclass
class UIEventInfo:
    iso_pos_track: Optional[PositionTracker] = None


ui_event_obj = UIEventInfo()
logger.info("ui_event_obj created")


# ./\       T~~~~~T
# /  \ ---\ |     |
# \  / ---/ |     |
# .\/       L_____J
# https://www.desmos.com/calculator/or2famsblw
def _get_transformed_mouse_pos(bb: BoundingBox) -> Tuple[float, float]:
    cam_bb = esper.component_for_entity(
        esper.get_component(GameCameraTag)[0][0], BoundingBox
    )
    display = pygame.display.get_surface()
    if display is None:
        raise RuntimeError("no display fond")
    display_rect = display.get_rect()
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0] * cam_bb.width / display_rect.width
    mouse_y = mouse[1] * cam_bb.height / display_rect.height
    map_width, map_height = map_obj.size

    mouse_in_bb_x = (mouse_x - bb.left) / bb.width
    mouse_in_bb_y = (mouse_y - bb.top) / bb.height

    x = (mouse_in_bb_x - mouse_in_bb_y) * (map_height + map_width) + map_width
    y = (mouse_in_bb_x + mouse_in_bb_y) * (map_height + map_width) - map_width
    return y / 2, x / 2


def click_on_tile(ent: int) -> None:
    bb = esper.component_for_entity(ent, BoundingBox)
    trans_mouse_pos = _get_transformed_mouse_pos(bb)
    mouse_bb = BoundingBox(
        trans_mouse_pos[0],
        trans_mouse_pos[0],
        trans_mouse_pos[1],
        trans_mouse_pos[1],
    )
    if ui_event_obj.iso_pos_track is None:
        raise RuntimeError("ui_event_obj iso_pos_track field missing")
    for intersect in ui_event_obj.iso_pos_track.intersect(mouse_bb):
        if intersect == ui_event_obj.iso_pos_track.plain:
            continue
        play_card(intersect)


def hover_over_tile(ent: int) -> None:
    bb = esper.component_for_entity(ent, BoundingBox)
    trans_mouse_pos = _get_transformed_mouse_pos(bb)
    mouse_bb = BoundingBox(
        trans_mouse_pos[0],
        trans_mouse_pos[0],
        trans_mouse_pos[1],
        trans_mouse_pos[1],
    )
    if ui_event_obj.iso_pos_track is None:
        raise RuntimeError("ui_event_obj iso_pos_track field missing")
    for intersect in ui_event_obj.iso_pos_track.intersect(mouse_bb):
        if intersect == ui_event_obj.iso_pos_track.plain:
            continue
        hover(intersect)
        return
    remove_hover(-1)
