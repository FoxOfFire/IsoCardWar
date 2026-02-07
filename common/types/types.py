from typing import Callable

EntityFunc = Callable[[int, int], None]
Action = Callable[[], None]
TextFunc = Callable[[], str]
