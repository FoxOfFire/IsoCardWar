from dataclasses import dataclass
from typing import Optional, Tuple, Type

import esper
import pygame

from common import SETTINGS_REF, BoundingBox
from layer2.tags import GameCameraTag

from .log import logger

SWITCH_SCENE = pygame.event.custom_type()


@dataclass
class UIEventInfo:
    iso_tag: Optional[Type] = None


ui_event_obj = UIEventInfo()
logger.info("ui_event_obj created")


# ./\       T~~~~~T
# /  \ ---\ |     |
# \  / ---/ |     |
# .\/       L_____J
# https://www.desmos.com/calculator/or2famsblw
def get_transformed_mouse_pos(bb: BoundingBox) -> Tuple[float, float]:
    cam_bb = esper.component_for_entity(
        esper.get_component(GameCameraTag)[0][0], BoundingBox
    )
    display = pygame.display.get_surface()
    assert display is not None

    display_rect = display.get_rect()
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0] * cam_bb.width / display_rect.width
    mouse_y = mouse[1] * cam_bb.height / display_rect.height

    map_width = SETTINGS_REF.ISO_MAP_HEIGHT
    map_height = SETTINGS_REF.ISO_MAP_WIDTH

    mouse_in_bb_x = (mouse_x - bb.left) / bb.width
    mouse_in_bb_y = (mouse_y - bb.top) / bb.height

    x = (mouse_in_bb_x - mouse_in_bb_y) * (map_height + map_width) + map_width
    y = (mouse_in_bb_x + mouse_in_bb_y) * (map_height + map_width) - map_width
    return y / 2, x / 2
