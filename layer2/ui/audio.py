from enum import StrEnum
from pathlib import Path
from typing import Dict

import pygame

from common import SETTINGS_REF

from .log import logger


class SoundTypeEnum(StrEnum):
    CLICK = "click"
    POP = "pop"
    TERRAFORM = "terraform"
    WHOOSH = "whoosh"
    MONEY = "money"


SFX_DIR = Path(".") / "layer2" / "ui" / "audio_assets"
SFX_AUDIO_DICT: Dict[SoundTypeEnum, pygame.mixer.Sound] = {}


def init_audio() -> None:
    for sound in [e for e in SoundTypeEnum]:
        logger.info(f"loaded sound: {sound}")
        file = SFX_DIR / f"{sound.value}.wav"
        SFX_AUDIO_DICT.update({sound: pygame.mixer.Sound(file)})
        SFX_AUDIO_DICT[sound].set_volume(0.05)
    SFX_AUDIO_DICT[SoundTypeEnum.POP].set_volume(0.2)
    SFX_AUDIO_DICT[SoundTypeEnum.TERRAFORM].set_volume(0.2)


def play_sfx(sound: SoundTypeEnum) -> None:
    if SETTINGS_REF.GAME_MUTE:
        return
    if sound not in SFX_AUDIO_DICT.keys():
        return
    logger.info(f"Playing sound:{sound}")
    SFX_AUDIO_DICT[sound].play()
