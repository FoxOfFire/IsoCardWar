from dataclasses import dataclass
from enum import IntEnum
from functools import partial
from typing import Dict, List, Tuple

from common import (
    SETTINGS_REF,
    WorldEnum,
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
    get_switch_world_action,
    quit_game,
    set_slider_val,
    toggle_sound,
)

from .spawner_ui import ButtonData
from .text_functions import (
    get_fps_str,
    get_game_phase_str,
    get_game_world_str,
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


MENU_LIST_DEF: Dict[WorldEnum, List[UIElementComponent]] = {}
MENU_DEF_REF: Dict[WorldEnum, List[MenuContainer]] = {
    WorldEnum.SETTINGS: [
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.CENTER, SnapVerticalEnum.CENTER),
            1,
            [
                ButtonData((6, 2), "Settings", UIElemType.TEXTBOX),
                ButtonData(
                    (6, 1),
                    "Mute Game",
                    UIElemType.CHECKBOX,
                    click_func=[toggle_sound],
                    button_default_data=SETTINGS_REF.GAME_MUTE,
                ),
                ButtonData(
                    (6, 1),
                    "Slider",
                    UIElemType.SLIDER,
                    button_default_data=0.5,
                    click_funcing=[set_slider_val],
                ),
                ButtonData(
                    (6, 1),
                    "Main Menu",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.MAIN)],
                ),
            ],
        ),
    ],
    WorldEnum.MAIN: [
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.CENTER, SnapVerticalEnum.CENTER),
            1,
            [
                ButtonData((6, 2), "Main Menu", UIElemType.TEXTBOX),
                ButtonData(
                    (6, 1),
                    "Continue",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.GAME)],
                ),
                ButtonData(
                    (6, 1),
                    "Settings",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.SETTINGS)],
                ),
                ButtonData(
                    (6, 1), "Quit", UIElemType.BUTTON, click_func=[quit_game]
                ),
            ],
        ),
    ],
    WorldEnum.GAME: [
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.RIGHT, SnapVerticalEnum.TOP),
            1,
            [
                ButtonData((6, 1), get_fps_str, UIElemType.TEXTBOX),
                ButtonData((6, 1), get_game_phase_str, UIElemType.TEXTBOX),
                ButtonData((6, 1), get_game_world_str, UIElemType.TEXTBOX),
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
                    "Main Menu",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.MAIN)],
                ),
            ],
        ),
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.LEFT, SnapVerticalEnum.TOP),
            1,
            [
                ButtonData((5, 2), "Debug", UIElemType.TEXTBOX),
                ButtonData(
                    (5, 1),
                    "End Turn",
                    UIElemType.BUTTON,
                    click_func=[end_player_phase_action],
                ),
                ButtonData(
                    (5, 1),
                    "Draw Card",
                    UIElemType.BUTTON,
                    click_func=[draw_card],
                ),
                ButtonData((5, 2), "Organise by", UIElemType.TEXTBOX),
                ButtonData(
                    (5, 1),
                    "Marker",
                    UIElemType.BUTTON,
                    click_func=[
                        sort_hand,
                        get_set_order_action(OrganizationEnum.MARKER),
                        sort_hand,
                    ],
                ),
                ButtonData(
                    (5, 1),
                    "Name",
                    UIElemType.BUTTON,
                    click_func=[
                        sort_hand,
                        get_set_order_action(OrganizationEnum.NAME),
                        sort_hand,
                    ],
                ),
                ButtonData(
                    (5, 1),
                    "None",
                    UIElemType.BUTTON,
                    click_func=[
                        sort_hand,
                        get_set_order_action(OrganizationEnum.NONE),
                        sort_hand,
                    ],
                ),
            ],
        ),
    ],
}
