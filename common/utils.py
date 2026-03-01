from dataclasses import dataclass
from math import pi, sin
from typing import Tuple


def lerp1(a: float, b: float, t: float) -> float:
    t = max(0, min(1, t))
    return (1 - t) * a + t * b


def lerp2(
    a: Tuple[float, float],
    b: Tuple[float, float],
    t: float,
    *,
    arch: float = 0
) -> Tuple[float, float]:
    ax, ay = a
    bx, by = b
    return (
        lerp1(ax, bx, t),
        lerp1(ay, by, t) - sin(pi * t) * arch,
    )


def add2i(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by


@dataclass
class Health:
    hp: float = 5
