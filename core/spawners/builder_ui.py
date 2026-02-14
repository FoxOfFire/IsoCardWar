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
)

from .spawner_ui import spawn_button
from .text_functions import (
    get_fps_str,
    get_game_phase_str,
    get_intersection_count,
    get_tracked_bb_of_type_str,
)


def build_ui() -> None:
    top_offset = 5
    if SETTINGS_REF.RENDER_FPS_UI:
        spawn_button(
            (top_offset, 5),
            (4, 1),
            get_fps_str,
            UIElemType.TEXTBOX,
        )
        top_offset += 4 * SETTINGS_REF.BUTTON_TILE_SIZE
    if SETTINGS_REF.RENDER_GAME_PHASE_UI:
        spawn_button(
            (top_offset, 5),
            (6, 1),
            get_game_phase_str,
            UIElemType.TEXTBOX,
        )
        top_offset += 6 * SETTINGS_REF.BUTTON_TILE_SIZE

    if SETTINGS_REF.RENDER_TRACKED_ISO_UI:
        spawn_button(
            (top_offset, 5),
            (5, 1),
            partial(get_tracked_bb_of_type_str, TrackIso, "TrackIso"),
            UIElemType.TEXTBOX,
        )
        top_offset += 5 * SETTINGS_REF.BUTTON_TILE_SIZE
    if SETTINGS_REF.RENDER_ISO_CAM_INTERSECT_UI:
        _, (cam_bb, _) = (esper.get_components(BoundingBox, IsoCameraTag))[0]
        spawn_button(
            (top_offset, 5),
            (5, 1),
            partial(get_intersection_count, "TrackIso", cam_bb, TrackIso),
            UIElemType.TEXTBOX,
        )
        top_offset += 5 * SETTINGS_REF.BUTTON_TILE_SIZE

    if SETTINGS_REF.RENDER_GAME_CAM_INTERSECT_UI:
        _, (cam_bb, _) = (esper.get_components(BoundingBox, GameCameraTag))[0]
        spawn_button(
            (top_offset, 5),
            (5, 1),
            partial(get_intersection_count, "TrackUI", cam_bb, TrackUI),
            UIElemType.TEXTBOX,
        )
        top_offset += 5 * SETTINGS_REF.BUTTON_TILE_SIZE
    if SETTINGS_REF.RENDER_TRACKED_UI_UI:
        spawn_button(
            (top_offset, 5),
            (5, 1),
            partial(get_tracked_bb_of_type_str, TrackUI, "TrackUI"),
            UIElemType.TEXTBOX,
        )
        top_offset += 5 * SETTINGS_REF.BUTTON_TILE_SIZE

    spawn_button(
            (5, 65),
            (3, 1),
            "Quit",
            UIElemType.BUTTON,
            click_func=[quit_game],
        )
    spawn_button(
        (5, 50),
        (4, 1),
        "End Turn",
        UIElemType.BUTTON,
        click_func=[end_player_phase_action],
    )
