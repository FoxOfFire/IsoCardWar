import json
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type

import esper
import pygame

from common import SETTINGS_REF, MarkerEnum
from layer1 import TerrainEnum, UnitTypeEnum
from layer2.tags import UIElementComponent

from .log import logger
from .utils import CardImageEnum, CardTypeEnum, UIElemSprite, UIElemType


class RenderAssetContainer:
    _BASE_ASSET_DIR = Path(".") / "layer2" / "rendering" / "assets"
    _UI_ASSETS_DIR = _BASE_ASSET_DIR / "ui"
    _CARD_ASSETS_DIR = _BASE_ASSET_DIR / "cards"
    _FONT_ASSET_DIR = _BASE_ASSET_DIR / "fonts"
    _ISO_ASSETS_DIR = _BASE_ASSET_DIR / "iso"

    _FONT: Optional[pygame.font.Font] = None

    _CARD_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _CARD_MARKER_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _CARD_IMAGE_SURFS: Dict[IntEnum, List[pygame.Surface]] = {}
    _CARD_SURFS: Dict[
        Tuple[IntEnum, IntEnum, IntEnum], List[pygame.Surface]
    ] = {}

    _TILE_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _UNIT_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _SELECTION_SURFS: Dict[IntEnum, pygame.Surface] = {}

    _BUTTON_TILE_MAPS: Dict[IntEnum, List[pygame.Surface]] = {}
    _BUTTON_SURFS: Dict[Tuple[IntEnum, int, int], List[pygame.Surface]] = {}

    def load_font(self) -> None:
        logger.info("loaded font")
        self._FONT = pygame.font.Font(
            self._FONT_ASSET_DIR / "tiny.ttf", SETTINGS_REF.FONT_SIZE
        )

    def draw_text_on_surf(self, screen: pygame.Surface, ent: int) -> None:
        assert esper.entity_exists(ent)
        assert self._FONT is not None

        ui_elem = esper.try_component(ent, UIElementComponent)
        assert ui_elem is not None

        for text in ui_elem.text:
            text_surf = self._FONT.render(
                text.text(), False, SETTINGS_REF.FONT_COLOR
            )
            screen.blit(text_surf, text_surf.get_rect(center=text.offset))

    def _load_card_surf(
        self, border: IntEnum, marker: IntEnum, image: IntEnum
    ) -> None:
        logger.info(f"added card{border.name, image.name, marker.name}")
        surfs = []
        for img_frame in self._CARD_IMAGE_SURFS[image]:
            surf: pygame.Surface = img_frame.copy()

            surf.blit(self._CARD_TYPE_SURFS[border])

            marker_surf = self._CARD_MARKER_SURFS[marker]
            surf.blit(
                marker_surf,
                marker_surf.get_rect(
                    topleft=(
                        SETTINGS_REF.RELATIVE_MARKER_POS_X,
                        SETTINGS_REF.RELATIVE_MARKER_POS_Y,
                    )
                ),
            )
            surfs.append(surf)
        self._CARD_SURFS.update({(border, marker, image): surfs})

    def get_card_surf(
        self, *, border: IntEnum, marker: IntEnum, image: IntEnum, frame: int
    ) -> pygame.Surface:
        surfs = self._CARD_SURFS.get((border, marker, image))
        if surfs is None:
            self._load_card_surf(border, marker, image)
            surfs = self._CARD_SURFS.get((border, marker, image))
            assert surfs is not None
        assert frame < len(surfs) and frame >= 0, frame
        return surfs[frame]

    def get_tile_type_surf(self, t: IntEnum) -> pygame.Surface:
        return self._TILE_TYPE_SURFS[t]

    def get_unit_type_surf(self, t: IntEnum) -> pygame.Surface:
        return self._UNIT_TYPE_SURFS[t]

    def get_selection_surf(self, t: IntEnum) -> pygame.Surface:
        return self._SELECTION_SURFS[t]

    def _get_rect_tile_surf(
        self,
        enum: UIElemType,
        /,
        *,
        rect: Tuple[int, int],
        offset: int,
        size: int,
    ) -> pygame.Surface:
        tilemap: List[pygame.Surface] = self._BUTTON_TILE_MAPS[enum]
        x, y = rect
        fin = pygame.Surface((x * size, y * size))
        fin.fill(pygame.Color(1, 0, 1, 1))
        tilemap_len = len(tilemap)
        for i in range(x):
            for j in range(y):
                tile = (offset * 16 + 15) % tilemap_len

                if j == 0:
                    tile -= 8
                if j == y - 1:
                    tile -= 4

                if i == 0:
                    tile -= 2
                if i == x - 1:
                    tile -= 1

                surf = tilemap[tile]
                fin.blit(surf, surf.get_rect(topleft=(i * size, j * size)))
        return fin

    def get_button_surf(self, sprite: UIElemSprite) -> List[pygame.Surface]:
        elem = sprite.elem_type
        x, y = sprite.size
        surfs = self._BUTTON_SURFS.get((elem, x, y))
        if surfs is None:
            surfs = []
            for i in range(3):
                surf = self._get_rect_tile_surf(
                    elem,
                    rect=(x, y),
                    offset=i,
                    size=SETTINGS_REF.BUTTON_TILE_SIZE,
                )
                surfs.append(surf)

        return surfs

    def _load_image_type(
        self,
        enum: Type[IntEnum],
        /,
        *,
        surfs: Dict[IntEnum, pygame.Surface],
        path: Path,
    ) -> None:
        logger.info(f"loaded image assets of type:{enum}")
        for e in enum:
            surfs.update(
                {
                    e: pygame.image.load(
                        path / f"{e.name.lower()}.png"
                    ).convert_alpha()
                }
            )

    def _load_image_types(self) -> None:
        self._load_image_type(
            CardTypeEnum,
            surfs=self._CARD_TYPE_SURFS,
            path=self._CARD_ASSETS_DIR,
        )
        self._load_image_type(
            MarkerEnum,
            surfs=self._CARD_MARKER_SURFS,
            path=self._CARD_ASSETS_DIR,
        )
        self._load_image_type(
            TerrainEnum,
            surfs=self._TILE_TYPE_SURFS,
            path=self._ISO_ASSETS_DIR,
        )
        self._load_image_type(
            UnitTypeEnum,
            surfs=self._UNIT_TYPE_SURFS,
            path=self._ISO_ASSETS_DIR,
        )
        self._load_image_type(
            MarkerEnum,
            surfs=self._SELECTION_SURFS,
            path=self._ISO_ASSETS_DIR,
        )

    def _load_animation_type(
        self,
        enum: Type[IntEnum],
        /,
        *,
        surfs: Dict[IntEnum, List[pygame.Surface]],
        path: Path,
    ) -> None:
        logger.info(f"loaded animation assets of type: {enum}")
        for images, frame_cnt in [(e, e.value) for e in enum]:
            surfs.update(
                {
                    images: [
                        pygame.image.load(
                            path / f"{images.name.lower()}{i+1}.png"
                        ).convert_alpha()
                        for i in range(frame_cnt)
                    ]
                }
            )

    def _load_anim_types(self) -> None:
        self._load_animation_type(
            CardImageEnum,
            surfs=self._CARD_IMAGE_SURFS,
            path=self._CARD_ASSETS_DIR,
        )

    def _load_tile_map(
        self,
        enum: Type[IntEnum],
        /,
        *,
        path: Path,
        surfs: Dict[IntEnum, List[pygame.Surface]],
    ) -> None:
        for name in enum:
            extracted_frames: List[pygame.Surface] = []
            with open(path / f"{name.name.lower()}.json", "r") as json_file:
                data = json.load(json_file)

                img_name = data["meta"]["image"]
                assert img_name == f"{name.name.lower()}.png", (
                    name.name.lower(),
                    img_name,
                )
                img = pygame.image.load(path / img_name).convert_alpha()

                frame_datas: List[Dict[str, Any]] = data["frames"]
                for frame_data in frame_datas:
                    info: Dict[str, int] = frame_data["frame"]
                    x = info["x"]
                    y = info["y"]
                    w = info["w"]
                    h = info["h"]
                    surf = pygame.Surface((w, h))
                    surf.blit(img, img.get_rect(topleft=(-x, -y)))
                    extracted_frames.append(surf)

            surfs[enum(name)] = extracted_frames

    def _load_tile_types(self) -> None:
        self._load_tile_map(
            UIElemType,
            surfs=self._BUTTON_TILE_MAPS,
            path=self._UI_ASSETS_DIR,
        )

    def load_images(self) -> None:
        self._load_image_types()
        self._load_anim_types()
        self._load_tile_types()


RENDER_ASSET_REF = RenderAssetContainer()
