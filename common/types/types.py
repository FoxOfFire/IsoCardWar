from typing import Callable

EntityFunc = Callable[[int, int], None]
ButtonFunc = Callable[[int], None]
PhaseFunc = Callable[[], None]
TextFunc = Callable[[], str]
