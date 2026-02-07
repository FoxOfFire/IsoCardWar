from typing import Callable, Optional

EntityFunc = Callable[[Optional[int], Optional[int]], None]
Action = Callable[[], None]
TextFunc = Callable[[], str]
