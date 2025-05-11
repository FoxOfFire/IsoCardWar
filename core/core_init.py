import argparse
import logging

import esper
import pygame

from common import BoundingBox, EventProcessor, PositionTracker
from layer1.cards import CardMovementProcessor, deck_obj, draw_card
from layer2 import GameCamera, Plain, WorldEnum
from layer2.rendering import (
    CardSprite,
    RenderingProcessor,
    RenderLayerEnum,
    load_images,
)
from layer2.ui import UIProcessor, bind_keyboard_events, init_audio

from . import global_vars
from .dying import DyingProcessor
from .event_handlers import bind_events as bind_core_events
from .log import logger
from .scene_switcher import SceneSwitcher
from .tracker_tags import TrackedByGameTracker, TrackedByUITracker

SEED = None


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
    game_plain = esper.create_entity(
        BoundingBox(
            0,
            10000,
            0,
            10000,
        ),
        Plain(),
    )
    display = pygame.display.get_surface()
    if display is None:
        raise RuntimeError("No screen found")
    UI_game_plain = esper.create_entity(
        BoundingBox(
            0,
            display.get_size()[0],
            0,
            display.get_size()[1],
        )
    )

    deck_obj.tracker_tag = TrackedByGameTracker
    deck_obj.sprite = CardSprite

    # Create processors
    ui_position_tracker = PositionTracker(TrackedByUITracker, UI_game_plain)
    game_position_tracker = PositionTracker(TrackedByGameTracker, game_plain)
    game_cam_bb = BoundingBox(0, 230, 0, 130)
    _ = esper.create_entity(game_cam_bb, GameCamera())

    card_movement_processor = CardMovementProcessor(game_cam_bb)

    render_layer_dict = {
        RenderLayerEnum.GAME: (game_position_tracker, BoundingBox(00, 230, 00, 130))
    }
    display_surf = pygame.display.get_surface()
    if display_surf is None:
        raise RuntimeError("Display failed to init")
    renderer = RenderingProcessor(display_surf, render_layer_dict, 8)

    event_processor = EventProcessor()
    ui_processor = UIProcessor(ui_position_tracker)

    dying_proc = DyingProcessor(game_position_tracker)
    scene_switcher = SceneSwitcher()

    bind_game_events(
        event_processor=event_processor,
        scene_switcher=scene_switcher,
    )

    esper.add_processor(event_processor)
    esper.add_processor(dying_proc)
    esper.add_processor(card_movement_processor)
    esper.add_processor(game_position_tracker)
    game_position_tracker.process()
    esper.add_processor(ui_position_tracker)
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

    logger.info("Finished init!!")

    draw_card()
    draw_card()
    draw_card()
    draw_card()
    draw_card()

    draw_card()
    draw_card()
    draw_card()
    draw_card()
    draw_card()
