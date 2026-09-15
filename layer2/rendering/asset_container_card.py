from enum import IntEnum
from typing import Dict, List, Optional, Tuple

import pygame

from common import SETTINGS_REF, PriceEnum
from layer1 import CardTypeEnum as CardType

from .log import logger
from .rendering_asset_loader import RENDER_ASSET_REF


class CardAssetContainer:

    _CARD_ASSETS_DIR = "cards"
    _CARD_TYPE_SURFS: List[pygame.Surface] = []
    _CARD_MARKER_SURFS: List[pygame.Surface] = []
    _CARD_IMAGE_SURFS: List[List[pygame.Surface]] = []
    _LOADED_CARD_SURFS: bool = False
    _CARD_SURFS: Dict[IntEnum, List[pygame.Surface]] = {}

    def get_saved_card_surf(
        self, frame: int, card_type: CardType
    ) -> Optional[pygame.Surface]:
        surfs = self._CARD_SURFS.get(card_type)
        if surfs is None:
            return None
        return surfs[frame]

    def get_card_surf(
        self,
        *,
        border: IntEnum,
        prices: Tuple[int, int, int, int],
        image: IntEnum,
        frame: int,
        card_type: CardType,
    ) -> pygame.Surface:
        surfs = self._CARD_SURFS.get(card_type)
        if surfs is None:
            if not self._LOADED_CARD_SURFS:
                self._load_anim_types()
                self._load_image_types()
                self._LOADED_CARD_SURFS = True

                if SETTINGS_REF.LOG_ASSET_LOADING:
                    logger.info("loaded card images")

            self._load_card_surf(border, prices, image, card_type)
            surfs = self._CARD_SURFS.get((card_type))
            assert surfs is not None
        assert frame < len(surfs) and frame >= 0, frame
        return surfs[frame]

    def _load_card_surf(
        self,
        border: IntEnum,
        prices: Tuple[int, int, int, int],
        image: IntEnum,
        card_type: CardType,
    ) -> None:
        if SETTINGS_REF.LOG_ASSET_LOADING:
            logger.info(f"added card{border.name, image.name, prices}")
        surfs = []
        for img_frame in self._CARD_IMAGE_SURFS[image.value - 1]:
            surf: pygame.Surface = img_frame.copy()

            surf.blit(self._CARD_TYPE_SURFS[border - 1])

            offset = 0
            for res in PriceEnum:
                for _ in range(prices[res.value - 1]):
                    marker_surf = self._CARD_MARKER_SURFS[res.value - 1]

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
        self._CARD_SURFS.update({card_type: surfs})

    def _load_anim_types(self) -> None:
        self._CARD_IMAGE_SURFS += [
            RENDER_ASSET_REF.load_tile_map(self._CARD_ASSETS_DIR, "card_arts")
        ]

    def _load_image_types(self) -> None:
        self._CARD_TYPE_SURFS += RENDER_ASSET_REF.load_tile_map(
            self._CARD_ASSETS_DIR, "card_borders"
        )
        self._CARD_MARKER_SURFS += RENDER_ASSET_REF.load_tile_map(
            self._CARD_ASSETS_DIR, "costs"
        )


CARD_ASSET_REF = CardAssetContainer()
