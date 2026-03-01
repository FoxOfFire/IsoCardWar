import json
from enum import IntEnum
from os.path import exists
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

import esper
import pygame

from common import SETTINGS_REF
from layer2.tags import UIElementComponent

from .log import logger


class RenderAssetContainer:
    _BASE_ASSET_DIR: Path = Path(".") / "layer2" / "rendering" / "assets"
    _FONT: Optional[pygame.font.Font] = None

    def draw_text_on_surf(self, screen: pygame.Surface, ent: int) -> None:
        if self._FONT is None:

            if SETTINGS_REF.LOG_ASSET_LOADING:
                logger.info("loaded font")
            self._FONT = pygame.font.Font(
                self._BASE_ASSET_DIR / "fonts" / "tiny.ttf",
                SETTINGS_REF.FONT_SIZE,
            )

        ui_elem = esper.component_for_entity(ent, UIElementComponent)

        for text in ui_elem.text:
            text_surf = self._FONT.render(
                text.text(), False, SETTINGS_REF.FONT_COLOR
            )
            screen.blit(text_surf, text_surf.get_rect(center=text.offset))

    def load_single_image(
        self,
        path: str,
        name: str,
    ) -> pygame.Surface:
        return pygame.image.load(
            self._BASE_ASSET_DIR / path / f"{name.lower()}.png"
        ).convert_alpha()

    def load_image_type(
        self,
        enum: Type[IntEnum],
        /,
        *,
        surfs: Dict[IntEnum, pygame.Surface],
        path: str,
    ) -> None:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"loaded image assets of type:{enum}")
        for e in enum:
            surfs.update(
                {
                    e: pygame.image.load(
                        self._BASE_ASSET_DIR / path / f"{e.name.lower()}.png"
                    ).convert_alpha()
                }
            )

    def load_animation_type(
        self,
        enum: Type[IntEnum],
        /,
        *,
        surfs: Dict[IntEnum, List[pygame.Surface]],
        path: str,
    ) -> None:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"loaded animation assets of type: {enum}")
        for images, frame_cnt in [(e, e.value) for e in enum]:
            surfs.update(
                {
                    images: [
                        pygame.image.load(
                            self._BASE_ASSET_DIR
                            / path
                            / f"{images.name.lower()}{i+1}.png"
                        ).convert_alpha()
                        for i in range(frame_cnt)
                    ]
                }
            )

    def load_tile_map(self, path: str, file_name: str) -> List[pygame.Surface]:
        extracted_frames: List[pygame.Surface] = []
        json_path, _ = (
            self._BASE_ASSET_DIR / path / f"{file_name}.json",
            "r",
        )
        if not exists(json_path):
            logger.warn(f"file does not exist: {path}/{file_name}.json")
            return []
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

    def load_tile_map_enum(
        self,
        enum: Type[IntEnum],
        /,
        *,
        path: str,
        surfs: Dict[IntEnum, List[pygame.Surface]],
    ) -> None:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"loaded tile assets of type: {enum}")
        for name in enum:
            extracted_frames = self.load_tile_map(path, name.name.lower())
            surfs.update({enum(name): extracted_frames})


RENDER_ASSET_REF = RenderAssetContainer()
