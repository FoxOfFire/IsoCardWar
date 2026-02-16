from functools import partial

import esper

from common import (
    SETTINGS_REF,
    BoundingBox,
    end_player_phase_action,
)
from layer2 import (
    GameCameraTag,
    IsoCameraTag,
    TrackIso,
    TrackUI,
    UIElemType,
    quit_game,
    set_slider_val,
    toggle_sound,
)

from .spawner_ui import spawn_button
from .text_functions import (
    get_fps_str,
    get_game_phase_str,
    get_intersection_count,
    get_tracked_bb_of_type_str,
)


def build_ui() -> None:
    spawn_button(
        (0, 0),
        (7, 10),
        "",
        UIElemType.MENU,
    )
    top_offset = 5
    if SETTINGS_REF.RENDER_FPS_UI:
        spawn_button(
            (5, top_offset),
            (4, 1),
            get_fps_str,
            UIElemType.TEXTBOX,
        )
        top_offset += SETTINGS_REF.BUTTON_TILE_SIZE
    if SETTINGS_REF.RENDER_GAME_PHASE_UI:
        spawn_button(
            (5, top_offset),
            (6, 1),
            get_game_phase_str,
            UIElemType.TEXTBOX,
        )
        top_offset += SETTINGS_REF.BUTTON_TILE_SIZE

    if SETTINGS_REF.RENDER_TRACKED_ISO_UI:
        spawn_button(
            (5, top_offset),
            (5, 1),
            partial(get_tracked_bb_of_type_str, TrackIso, "TrackIso"),
            UIElemType.TEXTBOX,
        )
        top_offset += SETTINGS_REF.BUTTON_TILE_SIZE
    if SETTINGS_REF.RENDER_ISO_CAM_INTERSECT_UI:
        _, (cam_bb, _) = (esper.get_components(BoundingBox, IsoCameraTag))[0]
        spawn_button(
            (5, top_offset),
            (5, 1),
            partial(get_intersection_count, "TrackIso", cam_bb, TrackIso),
            UIElemType.TEXTBOX,
        )
        top_offset += SETTINGS_REF.BUTTON_TILE_SIZE

    if SETTINGS_REF.RENDER_GAME_CAM_INTERSECT_UI:
        _, (cam_bb, _) = (esper.get_components(BoundingBox, GameCameraTag))[0]
        spawn_button(
            (5, top_offset),
            (5, 1),
            partial(get_intersection_count, "TrackUI", cam_bb, TrackUI),
            UIElemType.TEXTBOX,
        )
        top_offset += SETTINGS_REF.BUTTON_TILE_SIZE
    if SETTINGS_REF.RENDER_TRACKED_UI_UI:
        spawn_button(
            (5, top_offset),
            (5, 1),
            partial(get_tracked_bb_of_type_str, TrackUI, "TrackUI"),
            UIElemType.TEXTBOX,
        )
        top_offset += SETTINGS_REF.BUTTON_TILE_SIZE

    spawn_button(
        (5, top_offset),
        (4, 1),
        "End Turn",
        UIElemType.BUTTON,
        click_func=[end_player_phase_action],
    )
    top_offset += SETTINGS_REF.BUTTON_TILE_SIZE
    spawn_button(
        (5, top_offset),
        (5, 1),
        "Mute Game",
        UIElemType.CHECKBOX,
        click_func=[toggle_sound],
        button_default_data=SETTINGS_REF.GAME_MUTE,
    )
    top_offset += SETTINGS_REF.BUTTON_TILE_SIZE

    spawn_button(
        (5, top_offset),
        (4, 1),
        "Slider",
        UIElemType.SLIDER,
        button_default_data=0.5,
        click_funcing=[set_slider_val],
    )
    top_offset += SETTINGS_REF.BUTTON_TILE_SIZE
    spawn_button(
        (5, top_offset),
        (3, 1),
        "Quit",
        UIElemType.BUTTON,
        click_func=[quit_game],
    )
    top_offset += SETTINGS_REF.BUTTON_TILE_SIZE
