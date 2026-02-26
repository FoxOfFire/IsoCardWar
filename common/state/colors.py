from dataclasses import dataclass

from pygame import Color


@dataclass
class Colors:
    WHITE = Color("#f2f0e5")
    GRAY_WHITE = Color("#b8b5b9")
    GRAY_LIGHT = Color("#868188")
    GRAY = Color("#646365")
    GRAY_DARK = Color("#45444f")
    SHADE_LIGHT = Color("#5f556a")
    SHADE = Color("#4b4158")
    SHADE_DARK = Color("#352b42")
    BLACK = Color("#212123")
    SHADE_BLUE = Color("#3a3858")
    BLUE_DARK = Color("#43436a")
    BLUE = Color("#4b80ca")
    BLUE_LIGHT = Color("#68c2d3")
    BLUE_WHITE = Color("#a2dcc7")
    YELLOW = Color("#ede19e")
    BROWN_LIGHT = Color("#d3a068")
    BROWN = Color("#a77b5b")
    BROWN_DARK = Color("#80493a")
    RED = Color("#b45252")
    SWAMP_DARK = Color("#4e584a")
    SWAMP = Color("#7b7243")
    SWAMP_LIGHT = Color("#b2b47e")
    PASTEL = Color("#e5ceb4")
    GREEN_LIGHT = Color("#c2d368")
    GREEN = Color("#8ab060")
    GREEN_DARK = Color("#567b79")
    PURPLE_LIGHT = Color("#edc8c4")
    PURPLE = Color("#cf8acb")
    PURPLE_DARK = Color("#6a536e")
    TRANSPARENT = Color("#00000000")


COLOR_REF = Colors()
