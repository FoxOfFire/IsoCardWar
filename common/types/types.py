from typing import Callable, Optional

EntityFunc = Callable[[int, int], None]
ButtonFunc = Callable[[Optional[int], Optional[int]], None]
PhaseFunc = Callable[[], None]
TextFunc = Callable[[], str]
