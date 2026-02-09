import esper
import pygame

from common import RUN_DATA_REF, SETTINGS_REF

from .log import logger


def log_tick_performance() -> None:
    logger.info(f"current fps: {RUN_DATA_REF.game_clock.get_fps()}")
    logger.info(f"tick finished in: {RUN_DATA_REF.game_clock.get_rawtime()}ms")
    for proc_name in esper.process_times.keys():
        logger.info(
            f"{proc_name} finished in: {esper.process_times[proc_name]}"
        )


def run() -> None:
    RUN_DATA_REF.game_clock.tick(SETTINGS_REF.FPS)
    RUN_DATA_REF.game_clock.tick(SETTINGS_REF.FPS)
    while RUN_DATA_REF.game_running:
        esper.timed_process()
        pygame.display.flip()
        RUN_DATA_REF.game_clock.tick(SETTINGS_REF.FPS)
        if SETTINGS_REF.LOG_TICK_PERFORMANCE:
            log_tick_performance()
