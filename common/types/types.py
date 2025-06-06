from typing import Callable

ButtonFunc = Callable[[int, int], None]
EntityFunc = Callable[[int], None]
PhaseFunc = Callable[[], None]
TextFunc = Callable[[], str]
