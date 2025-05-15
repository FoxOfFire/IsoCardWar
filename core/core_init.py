import argparse
import logging

import esper
import pygame

from common import BoundingBox, EventProcessor, PositionTracker
from layer1.cards import CardMovementProcessor, deck_obj
from layer1.iso_map import make_map, map_obj
from layer2 import (
    GameCameraTag,
    IsoCameraTag,
    Plain,
    SceneSwitcher,
    UIElementComponent,
    WorldEnum,
)
from layer2.dying import DyingProcessor
from layer2.event_handlers import bind_events as bind_core_events
from layer2.rendering import (
    CardSprite,
    IsoSprite,
    RenderingProcessor,
    RenderLayerEnum,
    load_images,
)
from layer2.ui import UIProcessor, bind_keyboard_events, init_audio

from . import global_vars
from .log import logger
from .tracker_tags import TrackIso, TrackUI

GAME_CAM_WIDTH = 256
GAME_CAM_HEIGHT = 144
PIXEL_SIZE = 1080 / GAME_CAM_HEIGHT

SEED = None

ISO_MAP_HEIGHT = 8
ISO_MAP_WIDTH = 8


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


def init_globals() -> None:
    global_vars.game_clock = pygame.time.Clock()
    global_vars.game_running = True


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
        global_vars.game_running = False

    event_processor.bind(pygame.QUIT, handle_quit)


def init_game_world_esper() -> None:
    display = pygame.display.get_surface()
    if display is None:
        raise RuntimeError("No screen found")

    ui_plain = esper.create_entity(
        BoundingBox(
            -30,
            1000,
            -30,
            1000,
        ),
        Plain(),
    )
    iso_plain = esper.create_entity(
        BoundingBox(
            0,
            ISO_MAP_WIDTH,
            0,
            ISO_MAP_HEIGHT * 100,
        ),
        Plain(),
    )

    # dependency injection
    deck_obj.tracker_tag = TrackUI
    deck_obj.sprite = CardSprite
    deck_obj.ui_tag = UIElementComponent

    map_obj.tracker_tag = TrackIso
    map_obj.sprite = IsoSprite
    map_obj.size = (ISO_MAP_WIDTH, ISO_MAP_HEIGHT)

    # Create processors
    game_position_tracker = PositionTracker(TrackUI, ui_plain)
    iso_position_tracker = PositionTracker(TrackIso, iso_plain)

    game_cam_bb = BoundingBox(0, GAME_CAM_WIDTH, 0, GAME_CAM_HEIGHT)
    esper.create_entity(game_cam_bb, GameCameraTag())
    iso_cam_bb = BoundingBox(0, ISO_MAP_WIDTH, 0, ISO_MAP_HEIGHT)
    esper.create_entity(iso_cam_bb, IsoCameraTag())

    render_layer_dict = {
        RenderLayerEnum.CARD: (
            game_position_tracker,
            BoundingBox(00, GAME_CAM_WIDTH, 00, GAME_CAM_HEIGHT),
        ),
        RenderLayerEnum.ISO: (
            iso_position_tracker,
            BoundingBox(0, GAME_CAM_WIDTH, 0, GAME_CAM_HEIGHT),
        ),
    }
    renderer = RenderingProcessor(display, render_layer_dict, PIXEL_SIZE)

    card_movement_processor = CardMovementProcessor(game_cam_bb)
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

    esper.add_processor(iso_position_tracker)
    esper.add_processor(game_position_tracker)

    esper.add_processor(ui_processor)
    esper.add_processor(renderer)
    esper.add_processor(scene_switcher)


def init() -> None:
    init_logging()
    init_globals()
    init_window()
    init_audio()

    # game world
    esper.switch_world(WorldEnum.GAME)
    init_game_world_esper()
    load_images()
    esper.process()
    logger.info(f"{esper.current_world} world init finished")

    make_map()
    logger.info("Finished init!!")
