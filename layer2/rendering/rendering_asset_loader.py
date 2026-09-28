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

    def load_tile_map(
        self, path: str, name: str
    ) -> List[List[pygame.Surface]]:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(
                f"Loading tile map {self._BASE_ASSET_DIR}/{path}/{name}"
            )
        json_path, _ = (
            self._BASE_ASSET_DIR / path / f"{name}.json",
            "r",
        )
        assert exists(json_path), json_path
        with open(json_path) as json_file:
            data = json.load(json_file)

            metadata = data["meta"]
            img_name = metadata["image"]
            frame_tag_data = metadata["frameTags"]
            frame_crop_data: List[Dict[str, Any]] = data["frames"]

            assert img_name == f"{name}.png", (name, img_name)
            img = pygame.image.load(
                self._BASE_ASSET_DIR / path / img_name
            ).convert_alpha()

            extracted_frames: List[pygame.Surface] = []
            for crop_data in frame_crop_data:
                info: Dict[str, int] = crop_data["frame"]
                x = info["x"]
                y = info["y"]
                w = info["w"]
                h = info["h"]
                surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)
                surf.blit(img, img.get_rect(topleft=(-x, -y)))
                extracted_frames.append(surf)

            organised_frames: List[List[pygame.Surface]] = []
            for tag_data in frame_tag_data:
                begin: int = tag_data["from"]
                end: int = tag_data["to"] + 1
                tag_frames: List[pygame.Surface] = []
                for i in range(begin, end):
                    tag_frames.append(extracted_frames[i])
                organised_frames.append(tag_frames)

            return organised_frames


RENDER_ASSET_REF = RenderAssetContainer()
