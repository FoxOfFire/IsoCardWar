import json
from enum import IntEnum
from os.path import exists
from pathlib import Path
from typing import Any, Dict, List, Type

import pygame

from common import SETTINGS_REF

from .log import logger


class RenderAssetContainer:
    _BASE_ASSET_DIR: Path = Path(".") / "layer2" / "rendering" / "assets"

    def load_font(self, path: str, name: str) -> pygame.font.Font:
        return pygame.font.Font(
            self._BASE_ASSET_DIR / path / name,
            SETTINGS_REF.FONT_SIZE,
        )

    def load_tile_map(self, path: str, file_name: str) -> List[pygame.Surface]:
        extracted_frames: List[pygame.Surface] = []
        json_path, _ = (
            self._BASE_ASSET_DIR / path / f"{file_name}.json",
            "r",
        )
        assert exists(json_path), json_path
        with open(json_path) as json_file:
            data = json.load(json_file)

            img_name = data["meta"]["image"]
            assert img_name == f"{file_name}.png", (file_name, img_name)
            img = pygame.image.load(
                self._BASE_ASSET_DIR / path / img_name
            ).convert_alpha()

            frame_datas: List[Dict[str, Any]] = data["frames"]
            for frame_data in frame_datas:
                info: Dict[str, int] = frame_data["frame"]
                x = info["x"]
                y = info["y"]
                w = info["w"]
                h = info["h"]
                surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)
                surf.blit(img, img.get_rect(topleft=(-x, -y)))
                extracted_frames.append(surf)
        return extracted_frames


RENDER_ASSET_REF = RenderAssetContainer()
