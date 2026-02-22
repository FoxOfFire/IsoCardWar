from enum import IntEnum
from typing import Dict, List, Tuple

import pygame

from common import SETTINGS_REF, PriceEnum

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import CardImageEnum, CardTypeEnum


class CardAssetContainer:

    _CARD_ASSETS_DIR = "cards"
    _CARD_TYPE_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _CARD_MARKER_SURFS: Dict[IntEnum, pygame.Surface] = {}
    _CARD_IMAGE_SURFS: Dict[IntEnum, List[pygame.Surface]] = {}
    _LOADED_CARD_SURFS: bool = False
    _CARD_SURFS: Dict[
        Tuple[IntEnum, Tuple[int, int, int, int], IntEnum],
        List[pygame.Surface],
    ] = {}

    def get_card_surf(
        self,
        *,
        border: IntEnum,
        prices: Tuple[int, int, int, int],
        image: IntEnum,
        frame: int,
    ) -> pygame.Surface:
        surfs = self._CARD_SURFS.get((border, prices, image))
        if surfs is None:
            if not self._LOADED_CARD_SURFS:
                self._load_anim_types()
                self._load_image_types()
                self._LOADED_CARD_SURFS = True

                if SETTINGS_REF.LOG_ASSET_LOADING:
                    logger.info("loaded card images")

            self._load_card_surf(border, prices, image)
            surfs = self._CARD_SURFS.get((border, prices, image))
            assert surfs is not None
        assert frame < len(surfs) and frame >= 0, frame
        return surfs[frame]

    def _load_card_surf(
        self,
        border: IntEnum,
        prices: Tuple[int, int, int, int],
        image: IntEnum,
    ) -> None:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"added card{border.name, image.name, prices}")
        surfs = []
        for img_frame in self._CARD_IMAGE_SURFS[image]:
            surf: pygame.Surface = img_frame.copy()

            surf.blit(self._CARD_TYPE_SURFS[border])

            offset = 0
            for res in PriceEnum:
                for _ in range(prices[res.value - 1]):
                    marker_surf = self._CARD_MARKER_SURFS[res]

                    surf.blit(
                        marker_surf,
                        marker_surf.get_rect(
                            topleft=(
                                SETTINGS_REF.RELATIVE_MARKER_POS_X + offset,
                                SETTINGS_REF.RELATIVE_MARKER_POS_Y,
                            )
                        ),
                    )
                    offset += SETTINGS_REF.MARKER_OFFSET_X
            surfs.append(surf)
        self._CARD_SURFS.update({(border, prices, image): surfs})

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
            PriceEnum,
            surfs=self._CARD_MARKER_SURFS,
            path=self._CARD_ASSETS_DIR,
        )


CARD_ASSET_REF = CardAssetContainer()
