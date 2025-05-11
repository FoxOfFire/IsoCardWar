import esper
import pygame

from . import global_vars
from .log import logger


def log_tick_performance() -> None:
    logger.info(f"current fps: {global_vars.game_clock.get_fps()}")
    logger.info(f"tick finished in: {global_vars.game_clock.get_rawtime()}ms")
    for processor_name in esper.process_times.keys():
        logger.info(
            f"{processor_name} finished in: {esper.process_times[processor_name]}"
        )


def run() -> None:
    FPS = 60

    while global_vars.game_running:
        esper.timed_process()
        pygame.display.flip()
        global_vars.game_clock.tick(FPS)
        # log_tick_performance()
