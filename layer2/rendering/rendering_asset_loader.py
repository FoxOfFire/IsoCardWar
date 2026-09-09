import json
from os.path import exists
from pathlib import Path
from typing import Any, Dict, List

import pygame

from common import SETTINGS_REF

from .log import logger


class RenderAssetContainer:
    _BASE_ASSET_DIR: Path = Path(".") / "layer2" / "rendering" / "assets"

    def load_font(self, path: str, name: str) -> pygame.font.Font:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"Loading font {self._BASE_ASSET_DIR}/{path}/{name}")
        return pygame.font.Font(
            self._BASE_ASSET_DIR / path / name,
            SETTINGS_REF.FONT_SIZE,
        )

    def load_tile_map(self, path: str, name: str) -> List[pygame.Surface]:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(
                f"Loading tile map {self._BASE_ASSET_DIR}/{path}/{name}"
            )
        extracted_frames: List[pygame.Surface] = []
        json_path, _ = (
            self._BASE_ASSET_DIR / path / f"{name}.json",
            "r",
        )
        assert exists(json_path), json_path
        with open(json_path) as json_file:
            data = json.load(json_file)

            img_name = data["meta"]["image"]
            assert img_name == f"{name}.png", (name, img_name)
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
