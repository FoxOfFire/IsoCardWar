from dataclasses import dataclass
from enum import IntEnum
from functools import partial
from typing import List, Tuple

from common import (
    SETTINGS_REF,
    end_player_phase_action,
)
from layer1 import (
    OrganizationEnum,
    draw_card,
    get_set_order_action,
    sort_hand,
)
from layer2 import (
    TrackIso,
    TrackUI,
    UIElementComponent,
    UIElemType,
    flip_ui_elem_val,
    quit_game,
    set_slider_val,
    toggle_sound,
)

from .spawner_actions import get_toggle_menu_visibility
from .spawner_ui import ButtonData
from .text_functions import (
    get_fps_str,
    get_game_phase_str,
    get_tracked_bb_of_type_str,
)


class SnapHorisontalEnum(IntEnum):
    LEFT = 0
    CENTER = SETTINGS_REF.GAME_CAM_WIDTH // 2
    RIGHT = SETTINGS_REF.GAME_CAM_WIDTH


class SnapVerticalEnum(IntEnum):
    TOP = 0
    CENTER = SETTINGS_REF.GAME_CAM_HEIGHT // 2
    BOTTOM = SETTINGS_REF.GAME_CAM_HEIGHT


@dataclass
class MenuContainer:
    snap_point: Tuple[int, int]
    snap: Tuple[SnapHorisontalEnum, SnapVerticalEnum]
    edge_padding: int
    BUTTONS: List[ButtonData]


MENU_LIST_DEF: List[UIElementComponent] = []
MENU_DEF_REF = [
    MenuContainer(
        (0, 0),
        (SnapHorisontalEnum.RIGHT, SnapVerticalEnum.TOP),
        1,
        [
            ButtonData((6, 1), get_fps_str, UIElemType.TEXTBOX),
            ButtonData((6, 1), get_game_phase_str, UIElemType.TEXTBOX),
            ButtonData(
                (6, 1),
                partial(get_tracked_bb_of_type_str, TrackIso, "TrackIso"),
                UIElemType.TEXTBOX,
            ),
            ButtonData(
                (6, 1),
                partial(get_tracked_bb_of_type_str, TrackUI, "TrackUI"),
                UIElemType.TEXTBOX,
            ),
            ButtonData(
                (6, 1),
                "Quit",
                UIElemType.BUTTON,
                click_func=[quit_game],
            ),
        ],
    ),
    MenuContainer(
        (0, 0),
        (SnapHorisontalEnum.LEFT, SnapVerticalEnum.TOP),
        1,
        [
            ButtonData(
                (5, 1),
                "End Turn",
                UIElemType.BUTTON,
                click_func=[end_player_phase_action],
            ),
            ButtonData(
                (5, 1),
                "Mute Game",
                UIElemType.CHECKBOX,
                click_func=[toggle_sound],
                button_default_data=SETTINGS_REF.GAME_MUTE,
            ),
            ButtonData(
                (5, 1),
                "Slider",
                UIElemType.SLIDER,
                button_default_data=0.5,
                click_funcing=[set_slider_val],
            ),
            ButtonData(
                (5, 1),
                "Draw Card",
                UIElemType.BUTTON,
                click_func=[draw_card],
            ),
            ButtonData(
                (5, 1),
                "Organise:Marker",
                UIElemType.BUTTON,
                click_func=[
                    sort_hand,
                    get_set_order_action(OrganizationEnum.MARKER),
                    sort_hand,
                ],
            ),
            ButtonData(
                (5, 1),
                "Organise:Name",
                UIElemType.BUTTON,
                click_func=[
                    sort_hand,
                    get_set_order_action(OrganizationEnum.NAME),
                    sort_hand,
                ],
            ),
            ButtonData(
                (5, 1),
                "Organise:None",
                UIElemType.BUTTON,
                click_func=[
                    sort_hand,
                    get_set_order_action(OrganizationEnum.NONE),
                    sort_hand,
                ],
            ),
        ],
    ),
    MenuContainer(
        (0, 0),
        (SnapHorisontalEnum.CENTER, SnapVerticalEnum.TOP),
        1,
        [
            ButtonData(
                (5, 1),
                "Toggle menu1",
                UIElemType.CHECKBOX,
                click_func=[
                    get_toggle_menu_visibility(MENU_LIST_DEF, 0),
                    flip_ui_elem_val,
                ],
                button_default_data=True,
            ),
            ButtonData(
                (5, 1),
                "Toggle menu2",
                UIElemType.CHECKBOX,
                click_func=[
                    get_toggle_menu_visibility(MENU_LIST_DEF, 1),
                    flip_ui_elem_val,
                ],
                button_default_data=True,
            ),
        ],
    ),
]
