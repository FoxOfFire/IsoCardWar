from dataclasses import dataclass
from typing import Callable, Tuple


def _empty() -> str:
    return " "


@dataclass
class TextComponent:
    pos: Tuple[float, float]
    angle: float
    font_size: int
    text: Callable[[], str]

    @property
    def x(self) -> float:
        return self.pos[0]

    @property
    def y(self) -> float:
        return self.pos[1]


def text_component_from_str(
    text: str, pos: Tuple[float, float], angle: float, font_size: int
) -> TextComponent:
    def func() -> str:
        return text

    return TextComponent(pos, angle, font_size, func)
