import argparse
import logging

import esper
import pygame

from common import (
    GAME_CAM_HEIGHT,
    GAME_CAM_WIDTH,
    ISO_MAP_HEIGHT,
    ISO_MAP_WIDTH,
    POS_PROC_REF,
    RUN_DATA_REF,
    STARTER_DECK_COUNT,
    BBMoveProcessor,
    BoundingBox,
    EventProcessor,
)
from layer1 import (
    DECK_REF,
    CardMovementProcessor,
    GamePhaseProcessor,
    create_starting_deck,
    draw_card,
)
from layer2 import (
    DyingProcessor,
    GameCameraTag,
    IsoCameraTag,
    IsoSprite,
    RenderingProcessor,
    SceneSwitcher,
    TrackIso,
    TrackUI,
    UIProcessor,
    WorldEnum,
    bind_events,
    bind_keyboard_events,
    init_audio,
    load_images,
    ui_event_obj,
)

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
        prog="IsoCardWar",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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

    window_dimension = (1980, 1080)

    pygame.display.set_mode(
        size=window_dimension,
        flags=pygame.DOUBLEBUF | pygame.FULLSCREEN,
    )


def bind_game_events(
    event_processor: EventProcessor,
    scene_switcher: SceneSwitcher,
) -> None:
    bind_events(event_processor, scene_switcher)
    bind_keyboard_events(event_processor)

    def handle_quit(_: pygame.event.Event) -> None:
        RUN_DATA_REF.game_running = False

    event_processor.bind(pygame.QUIT, handle_quit)


def init_game_world_esper() -> None:
    display = pygame.display.get_surface()
    assert display is not None

    # Create processors
    POS_PROC_REF.start_tracking_type(TrackIso)
    POS_PROC_REF.start_tracking_type(TrackUI)
    mov_processor: BBMoveProcessor = BBMoveProcessor()

    game_cam_bb = BoundingBox(0, GAME_CAM_WIDTH, 0, GAME_CAM_HEIGHT)
    esper.create_entity(game_cam_bb, GameCameraTag())
    iso_cam_bb = BoundingBox(0, ISO_MAP_HEIGHT, 0, ISO_MAP_WIDTH)
    esper.create_entity(iso_cam_bb, IsoCameraTag())

    renderer = RenderingProcessor(display)

    card_movement_processor = CardMovementProcessor(game_cam_bb)
    game_phase_processor = GamePhaseProcessor(get_base_game_phase_dict())
    event_processor = EventProcessor()
    ui_processor = UIProcessor(display.get_size())

    dying_proc = DyingProcessor()
    scene_switcher = SceneSwitcher()

    bind_game_events(
        event_processor=event_processor,
        scene_switcher=scene_switcher,
    )

    POS_PROC_REF.process()

    # adding processors
    esper.add_processor(event_processor)
    esper.add_processor(card_movement_processor)
    esper.add_processor(game_phase_processor)

    esper.add_processor(mov_processor)
    esper.add_processor(POS_PROC_REF)

    esper.add_processor(ui_processor)
    esper.add_processor(renderer)
    esper.add_processor(dying_proc)
    esper.add_processor(scene_switcher)

    # dependency injection
    DECK_REF.spawn_card = spawn_card_ent
    DECK_REF.create_card = create_card_obj
    create_starting_deck(STARTER_DECK_COUNT)
    for _ in range(7):
        draw_card()

    spawn_iso_elem(TrackIso, TrackUI, IsoSprite)

    ui_event_obj.iso_tag = TrackIso


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

    logger.info(
        "\n\n----------------------< Finished Init >----------------------\n"
    )
