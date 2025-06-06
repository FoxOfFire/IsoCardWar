import argparse
import logging

import esper
import pygame

from common import BoundingBox, EventProcessor, PositionTracker
from common.constants import (
    GAME_CAM_HEIGHT,
    GAME_CAM_WIDTH,
    ISO_MAP_HEIGHT,
    ISO_MAP_WIDTH,
    STARTER_DECK_COUNT,
)
from common.globals import RUN_DATA_REF
from layer1.cards import (
    DECK_REF,
    CardMovementProcessor,
    create_starting_deck,
    draw_card,
)
from layer1.game_phase import GamePhaseProcessor
from layer2 import (
    GameCameraTag,
    IsoCameraTag,
    Plain,
    SceneSwitcher,
    TrackIso,
    TrackUI,
    WorldEnum,
    ui_event_obj,
)
from layer2.dying import DyingProcessor
from layer2.event_handlers import bind_events as bind_core_events
from layer2.rendering import (
    IsoSprite,
    RenderingProcessor,
    RenderLayerEnum,
    UIElemType,
    load_images,
)
from layer2.ui import UIProcessor, bind_keyboard_events, init_audio

from .log import logger
from .spawners import (
    build_ui,
    create_card_obj,
    get_base_game_phase_dict,
    spawn_card_ent,
    spawn_iso_elem,
)


def init_logging() -> None:
    parser = argparse.ArgumentParser(
        prog="Safari", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-ll", "--log-level", default=logging.INFO)
    parser.add_argument("-lf", "--log-file", default=None)
    args = parser.parse_args()
    format = "%(levelname)s: (%(asctime)s): [%(name)s]: %(message)s"
    logging.basicConfig(
        level=args.log_level,
        filename=args.log_file,
        format=format,
        filemode="w",
    )


def init_window() -> None:
    pygame.init()

    window_dimension = (1920, 1080)
    if window_dimension not in pygame.display.list_modes():
        raise RuntimeError("Screen is not supported")

    pygame.display.set_mode(
        size=window_dimension,
        flags=pygame.DOUBLEBUF | pygame.FULLSCREEN,
    )


def bind_game_events(
    event_processor: EventProcessor,
    scene_switcher: SceneSwitcher,
) -> None:
    bind_core_events(event_processor, scene_switcher)
    bind_keyboard_events(event_processor)

    def handle_quit(event: pygame.event.Event) -> None:
        RUN_DATA_REF.game_running = False

    event_processor.bind(pygame.QUIT, handle_quit)


def init_game_world_esper() -> None:
    display = pygame.display.get_surface()
    if display is None:
        raise RuntimeError("No screen found")

    ui_plain = esper.create_entity(
        BoundingBox(
            -100,
            1000,
            -100,
            1000,
        ),
        Plain(),
    )
    iso_plain = esper.create_entity(
        BoundingBox(
            0,
            ISO_MAP_HEIGHT,
            0,
            ISO_MAP_WIDTH,
        ),
        Plain(),
    )

    # Create processors
    game_position_tracker = PositionTracker(TrackUI, ui_plain)
    iso_position_tracker = PositionTracker(TrackIso, iso_plain)

    game_cam_bb = BoundingBox(0, GAME_CAM_WIDTH, 0, GAME_CAM_HEIGHT)
    esper.create_entity(game_cam_bb, GameCameraTag())
    iso_cam_bb = BoundingBox(0, ISO_MAP_HEIGHT, 0, ISO_MAP_WIDTH)
    esper.create_entity(iso_cam_bb, IsoCameraTag())

    render_layer_dict = {
        RenderLayerEnum.CARD: (
            game_position_tracker,
            BoundingBox(0, GAME_CAM_WIDTH, 0, GAME_CAM_HEIGHT),
        ),
        RenderLayerEnum.ISO: (
            iso_position_tracker,
            BoundingBox(0, GAME_CAM_WIDTH, 0, GAME_CAM_HEIGHT),
        ),
    }
    renderer = RenderingProcessor(display, render_layer_dict)

    card_movement_processor = CardMovementProcessor(game_cam_bb)
    game_phase_processor = GamePhaseProcessor(get_base_game_phase_dict())
    event_processor = EventProcessor()
    ui_processor = UIProcessor(game_position_tracker, display.get_size())

    dying_proc = DyingProcessor(game_position_tracker)
    scene_switcher = SceneSwitcher()

    bind_game_events(
        event_processor=event_processor,
        scene_switcher=scene_switcher,
    )

    game_position_tracker.process()

    # adding processors
    esper.add_processor(event_processor)
    esper.add_processor(dying_proc)
    esper.add_processor(card_movement_processor)
    esper.add_processor(game_phase_processor)

    esper.add_processor(iso_position_tracker)
    esper.add_processor(game_position_tracker)

    esper.add_processor(ui_processor)
    esper.add_processor(renderer)
    esper.add_processor(scene_switcher)

    # dependency injection
    DECK_REF.spawn_card = spawn_card_ent
    DECK_REF.create_card = create_card_obj
    create_starting_deck(STARTER_DECK_COUNT)
    for _ in range(7):
        draw_card()

    spawn_iso_elem(TrackIso, TrackUI, IsoSprite)

    ui_event_obj.iso_pos_track = iso_position_tracker


def init() -> None:
    init_logging()
    init_window()
    init_audio()

    # game world
    esper.switch_world(WorldEnum.GAME.value)
    init_game_world_esper()
    load_images()
    esper.process()
    build_ui()
    logger.info(f"{esper.current_world} world init finished")
    spawn_button((20, 40), "Penis!!", UIElemType.TEXTBOX)
    spawn_button((20, 52), "Cocking", UIElemType.BUTTON)

    logger.info("Finished init!!")
