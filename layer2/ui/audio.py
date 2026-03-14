from enum import IntEnum, auto
from pathlib import Path
from typing import Dict

import pygame

from common import SETTINGS_REF

from .log import logger


class SoundTypeEnum(IntEnum):
    CLICK = auto()
    POP = auto()
    TERRAFORM = auto()
    WHOOSH = auto()
    MONEY = auto()


SFX_DIR = Path(".") / "layer2" / "ui" / "audio_assets"
SFX_AUDIO_DICT: Dict[SoundTypeEnum, pygame.mixer.Sound] = {}


def init_audio() -> None:
    for sound in [e for e in SoundTypeEnum]:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"loaded sound: {sound.name}")
        file = SFX_DIR / f"{sound.name.lower()}.wav"
        SFX_AUDIO_DICT.update({sound: pygame.mixer.Sound(file)})
    set_master_vol(1)


def set_master_vol(vol: float) -> None:
    for sound in [e for e in SoundTypeEnum]:
        SFX_AUDIO_DICT[sound].set_volume(vol)


def play_sfx(sound: SoundTypeEnum) -> bool:
    if SETTINGS_REF.GAME_MUTE:
        return False
    if sound not in SFX_AUDIO_DICT.keys():
        return False
    if SETTINGS_REF.LOG_PLAY_SOUND:
        logger.info(f"Playing sound:{sound.name}")
    SFX_AUDIO_DICT[sound].play()
    return True
