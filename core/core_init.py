import argparse
import logging

import esper
import pygame

from common import (
    BB_MOVE_PROC_REF,
    EVENT_PROC_REF,
    POS_PROC_REF,
    RUN_DATA_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
    PriceEnum,
    WorldEnum,
)
from layer1 import (
    CARD_MOV_PROC_REF,
    DECK_REF,
    GAME_PHASE_PROC_REF,
    PARTICLE_PROC_REF,
    end_phase,
)
from layer2 import (
    DYING_PROC_REF,
    RENDER_PROC_REF,
    SCENE_SWITCH_PROC_REF,
    UI_EVENT_REF,
    UI_PROC_REF,
    GameCameraTag,
    IsoCameraTag,
    IsoSprite,
    TrackIso,
    TrackUI,
    bind_keyboard_events,
    init_audio,
)
from layer3 import (
    UI_BUILDER_REF,
    create_card_obj,
    get_base_game_phase_dict,
    set_type_actions,
    spawn_card_ent,
    spawn_iso_elem,
)

from .log import logger


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

    if SETTINGS_REF.GAME_FULLSCREEN:
        window_dimension = (1980, 1080)
        pygame.display.set_mode(
            size=window_dimension,
            flags=pygame.DOUBLEBUF | pygame.FULLSCREEN,
        )
    else:
        window_dimension = (1280, 720)
        pygame.display.set_mode(size=window_dimension, flags=pygame.DOUBLEBUF)


def bind_game_events() -> None:
    bind_keyboard_events()

    def handle_quit(_: pygame.event.Event) -> None:
        RUN_DATA_REF.game_running = False

    EVENT_PROC_REF.bind(pygame.QUIT, handle_quit)


def init_processors(*, game_proc: bool = False) -> None:  # adding processors

    if game_proc:
        esper.add_processor(CARD_MOV_PROC_REF)

    esper.add_processor(BB_MOVE_PROC_REF())
    esper.add_processor(POS_PROC_REF())
    esper.add_processor(EVENT_PROC_REF)
    esper.add_processor(UI_PROC_REF())
    esper.add_processor(PARTICLE_PROC_REF())

    if game_proc:
        esper.add_processor(GAME_PHASE_PROC_REF)

    esper.add_processor(RENDER_PROC_REF())
    esper.add_processor(DYING_PROC_REF)
    esper.add_processor(SCENE_SWITCH_PROC_REF)


def init_world(*, game_ents: bool = False) -> None:
    display = pygame.display.get_surface()
    assert display is not None

    game_cam_bb = BoundingBox(
        0, SETTINGS_REF.GAME_CAM_WIDTH, 0, SETTINGS_REF.GAME_CAM_HEIGHT
    )
    esper.create_entity(game_cam_bb, GameCameraTag())

    if game_ents:
        iso_cam_bb = BoundingBox(
            0, SETTINGS_REF.ISO_MAP_HEIGHT, 0, SETTINGS_REF.ISO_MAP_WIDTH
        )
        esper.create_entity(iso_cam_bb, IsoCameraTag())

        spawn_iso_elem(TrackIso, TrackUI, IsoSprite)

        POS_PROC_REF().start_tracking_type(TrackIso)
        POS_PROC_REF().start_tracking_type(TrackUI)
        for phase, func_list in get_base_game_phase_dict().items():
            GAME_PHASE_PROC_REF.add_game_phase(phase, func_list=func_list)
        GAME_PHASE_PROC_REF.set_end_phase(end_phase)

        set_type_actions()

        CARD_MOV_PROC_REF.set_cam_bb(game_cam_bb)

    RENDER_PROC_REF().set_display_and_init_cam_types(display)

    UI_PROC_REF().set_display_size(display.get_size())
    UI_PROC_REF().set_tracker_tag(TrackUI)

    UI_BUILDER_REF.build_ui()


def init_game() -> None:
    display = pygame.display.get_surface()
    assert display is not None

    DECK_REF.spawn_card = spawn_card_ent
    DECK_REF.create_card = create_card_obj
    DECK_REF.create_starting_deck()

    UI_EVENT_REF.iso_tag = TrackIso

    STATE_REF.resources.update(
        {
            PriceEnum.MANA: SETTINGS_REF.DEFAULT_RESOURCE_MANA,
            PriceEnum.HERBS: SETTINGS_REF.DEFAULT_RESOURCE_HERBS,
            PriceEnum.BLOOD: SETTINGS_REF.DEFAULT_RESOURCE_BLOOD,
            PriceEnum.BREW: SETTINGS_REF.DEFAULT_RESOURCE_BREW,
        }
    )


def init() -> None:
    init_logging()
    init_window()
    init_audio()

    init_game()
    bind_game_events()

    # game world
    SCENE_SWITCH_PROC_REF.switch_world_to(WorldEnum.GAME)
    SCENE_SWITCH_PROC_REF.process()
    init_processors(game_proc=True)
    init_world(game_ents=True)

    # menu world
    SCENE_SWITCH_PROC_REF.switch_world_to(WorldEnum.SETTINGS)
    SCENE_SWITCH_PROC_REF.process()
    init_processors()
    init_world()

    # menu world
    SCENE_SWITCH_PROC_REF.switch_world_to(WorldEnum.MAIN)
    SCENE_SWITCH_PROC_REF.process()
    init_processors()
    init_world()

    logger.info(f"{esper.current_world} world init finished")

    logger.info(
        "\n\n----------------------< Finished Init >----------------------\n"
    )
