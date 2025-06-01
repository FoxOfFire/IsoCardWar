import pygame


class RunData:
    game_running: bool = True
    game_clock: pygame.time.Clock = pygame.time.Clock()

    @property
    def delta_time(self) -> int:
        time = self.game_clock.get_time()
        if time == 0:
            time = 3
        return time


RUN_DATA_REF = RunData()
