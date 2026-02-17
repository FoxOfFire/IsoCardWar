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
    UIElemType,
    quit_game,
    set_slider_val,
    toggle_sound,
)

from .spawner_ui import ButtonData, spawn_button
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
class Menu:
    snap_point: Tuple[int, int]
    snap: Tuple[SnapHorisontalEnum, SnapVerticalEnum]
    edge_padding: int
    BUTTONS: List[ButtonData]


MENU_KETTO_REF = Menu(
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
)
MENU_REF = Menu(
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
)


def _snap(snap: IntEnum, size: int, cam_size: int) -> int:
    offset = (snap.value * 2) // cam_size
    ret = snap.value - (offset * size // 2)
    return ret


def _build_menu(menu: Menu) -> None:
    menu_width: int = 0
    menu_height: int = 0
    for button in menu.BUTTONS:
        w, h = button.size
        menu_width = max(menu_width, w)
        menu_height += h
    menu_width += menu.edge_padding
    menu_height += menu.edge_padding

    snap_w, snap_h = menu.snap
    x, y = menu.snap_point

    x += _snap(
        snap_w,
        menu_width * SETTINGS_REF.BUTTON_TILE_SIZE,
        SETTINGS_REF.GAME_CAM_WIDTH,
    )
    y += _snap(
        snap_h,
        menu_height * SETTINGS_REF.BUTTON_TILE_SIZE,
        SETTINGS_REF.GAME_CAM_HEIGHT,
    )

    spawn_button(
        (x, y),
        ButtonData((menu_width, menu_height), "", UIElemType.MENU),
    )

    w_offset = menu.edge_padding * SETTINGS_REF.BUTTON_TILE_SIZE // 2 + x
    h_offset = menu.edge_padding * SETTINGS_REF.BUTTON_TILE_SIZE // 2 + y
    for button in menu.BUTTONS:
        _, h = button.size
        spawn_button((w_offset, h_offset), button)
        h_offset += (h) * SETTINGS_REF.BUTTON_TILE_SIZE


def build_ui() -> None:
    _build_menu(MENU_REF)
    _build_menu(MENU_KETTO_REF)
