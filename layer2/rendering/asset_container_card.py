from enum import IntEnum
from typing import Dict, List, Tuple

import pygame

from common import SETTINGS_REF, MarkerEnum

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import CardImageEnum, CardTypeEnum


class CardAssetContainer:

    _CARD_ASSETS_DIR = "cards"
    _CARD_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _CARD_MARKER_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _CARD_IMAGE_SURFS: Dict[IntEnum, List[pygame.Surface]] = {}
    _CARD_SURFS: Dict[
        Tuple[IntEnum, IntEnum, IntEnum], List[pygame.Surface]
    ] = {}

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

    def _load_anim_types(self) -> None:
        RENDER_ASSET_REF.load_animation_type(
            CardImageEnum,
            surfs=self._CARD_IMAGE_SURFS,
            path=self._CARD_ASSETS_DIR,
        )

    def _load_image_types(self) -> None:
        RENDER_ASSET_REF.load_image_type(
            CardTypeEnum,
            surfs=self._CARD_TYPE_SURFS,
            path=self._CARD_ASSETS_DIR,
        )
        RENDER_ASSET_REF.load_image_type(
            MarkerEnum,
            surfs=self._CARD_MARKER_SURFS,
            path=self._CARD_ASSETS_DIR,
        )

    def load_images(self) -> None:
        self._load_anim_types()
        self._load_image_types()


CARD_ASSET_REF = CardAssetContainer()
