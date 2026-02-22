from dataclasses import dataclass
from enum import IntEnum
from functools import partial
from typing import Dict, List, Tuple

from common import (
    SETTINGS_REF,
    PriceEnum,
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
    get_resource_amount,
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
    BUTTONS: List[ButtonData | Tuple[int, int]]
    align_horizontal: bool = False


MENU_LIST_DEF: Dict[WorldEnum, List[UIElementComponent]] = {}
MENU_DEF_REF: Dict[WorldEnum, List[MenuContainer]] = {
    WorldEnum.SETTINGS: [
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.CENTER, SnapVerticalEnum.CENTER),
            4,
            [
                ButtonData("Settings", UIElemType.TEXTBOX, (6, 1), (0, 4)),
                (0, 4),
                ButtonData(
                    "Mute Game",
                    UIElemType.CHECKBOX,
                    click_func=[toggle_sound],
                    button_default_data=SETTINGS_REF.GAME_MUTE,
                ),
                (0, 1),
                ButtonData(
                    "Slider",
                    UIElemType.SLIDER,
                    button_default_data=0.5,
                    click_funcing=[set_slider_val],
                ),
                (0, 2),
                ButtonData(
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
            4,
            [
                ButtonData("Main Menu", UIElemType.TEXTBOX, (6, 1), (0, 6)),
                (0, 4),
                ButtonData(
                    "Continue",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.GAME)],
                ),
                (0, 1),
                ButtonData(
                    "Settings",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.SETTINGS)],
                ),
                (0, 5),
                ButtonData("Quit", UIElemType.BUTTON, click_func=[quit_game]),
            ],
        ),
    ],
    WorldEnum.GAME: [
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.CENTER, SnapVerticalEnum.TOP),
            4,
            [
                ButtonData(
                    partial(get_resource_amount, PriceEnum.MANA),
                    UIElemType.ICON,
                    (3, 1),
                    button_default_data=0,
                ),
                (2, 0),
                ButtonData(
                    partial(get_resource_amount, PriceEnum.HERBS),
                    UIElemType.ICON,
                    (3, 1),
                    button_default_data=1,
                ),
                (2, 0),
                ButtonData(
                    partial(get_resource_amount, PriceEnum.BLOOD),
                    UIElemType.ICON,
                    (3, 1),
                    button_default_data=2,
                ),
                (2, 0),
                ButtonData(
                    partial(get_resource_amount, PriceEnum.BREW),
                    UIElemType.ICON,
                    (3, 1),
                    button_default_data=3,
                ),
            ],
            True,
        ),
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.RIGHT, SnapVerticalEnum.TOP),
            4,
            [
                ButtonData("Info", UIElemType.TEXTBOX, (6, 1), (0, 4)),
                (0, 4),
                ButtonData(get_fps_str, UIElemType.TEXTBOX),
                (0, 1),
                ButtonData(get_game_phase_str, UIElemType.TEXTBOX),
                (0, 1),
                ButtonData(get_game_world_str, UIElemType.TEXTBOX),
                (0, 4),
                ButtonData(
                    partial(get_tracked_bb_of_type_str, TrackIso, "TrackIso"),
                    UIElemType.TEXTBOX,
                ),
                (0, 1),
                ButtonData(
                    partial(get_tracked_bb_of_type_str, TrackUI, "TrackUI"),
                    UIElemType.TEXTBOX,
                ),
                (0, 4),
            ],
        ),
        MenuContainer(
            (0, 0),
            (SnapHorisontalEnum.LEFT, SnapVerticalEnum.TOP),
            4,
            [
                ButtonData("Menu", UIElemType.TEXTBOX, (6, 1), (0, 4)),
                (0, 2),
                ButtonData(
                    "Main Menu",
                    UIElemType.BUTTON,
                    click_func=[get_switch_world_action(WorldEnum.MAIN)],
                ),
                (0, 5),
                ButtonData("Debug", UIElemType.TEXTBOX, sub_size=(0, 4)),
                (0, 2),
                ButtonData(
                    "End Turn",
                    UIElemType.BUTTON,
                    click_func=[end_player_phase_action],
                ),
                (0, 1),
                ButtonData(
                    "Draw Card",
                    UIElemType.BUTTON,
                    click_func=[draw_card],
                ),
                (0, 4),
                ButtonData("Organise by", UIElemType.TEXTBOX, sub_size=(0, 4)),
                (0, 2),
                ButtonData(
                    "Marker",
                    UIElemType.BUTTON,
                    click_func=[
                        sort_hand,
                        get_set_order_action(OrganizationEnum.MARKER),
                        sort_hand,
                    ],
                ),
                (0, 1),
                ButtonData(
                    "Name",
                    UIElemType.BUTTON,
                    click_func=[
                        sort_hand,
                        get_set_order_action(OrganizationEnum.NAME),
                        sort_hand,
                    ],
                ),
                (0, 1),
                ButtonData(
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
