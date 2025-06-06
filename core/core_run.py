import esper
import pygame

from common.constants import FPS
from common.globals import RUN_DATA_REF

from .log import logger


def log_tick_performance() -> None:
    logger.info(f"current fps: {RUN_DATA_REF.game_clock.get_fps()}")
    logger.info(f"tick finished in: {RUN_DATA_REF.game_clock.get_rawtime()}ms")
    for processor_name in esper.process_times.keys():
        logger.info(
            f"{processor_name} finished in: {esper.process_times[processor_name]}"
        )


def run() -> None:
    RUN_DATA_REF.game_clock.tick(FPS)
    RUN_DATA_REF.game_clock.tick(FPS)
    while RUN_DATA_REF.game_running:
        esper.timed_process()
        pygame.display.flip()
        RUN_DATA_REF.game_clock.tick(FPS)
        # log_tick_performance()
