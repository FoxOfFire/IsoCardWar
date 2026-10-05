import json
from enum import IntEnum
from os.path import exists
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type

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

    def _greatest_common_divisor(self, a: int, b: int) -> int:
        while a != b:
            if a > b:
                a -= b
            else:
                b -= a
        return a

    def _lowest_common_multiple_of_list(self, int_list: List[int]) -> int:
        res: int = 1
        for n in int_list:
            gcd = self._greatest_common_divisor(n, res)
            res = (res * n) // gcd
        return res

    def _enum_permutator(
        self,
        meta: List[Tuple[Type[IntEnum], int, int]],
    ) -> List[List[int]]:
        enum_permutations: List[List[int]] = [[]]

        for i in range(len(meta)):
            new_permutations: List[List[int]] = []
            for perm in enum_permutations:
                for curr_enum in [None] + list(meta[i][0]):
                    next_item = perm.copy()
                    if curr_enum is None:
                        next_item.append(0)
                    else:
                        next_item.append(meta[i][0](curr_enum).value)
                    new_permutations.append(next_item)
            enum_permutations = new_permutations
        return enum_permutations

    def create_animation(
        self,
        size: Tuple[int, int],
        meta: List[Tuple[Type[IntEnum], int, int]],
        frames: List[List[List[pygame.Surface]]],
    ) -> Dict[
        Tuple[Optional[IntEnum], ...],
        List[Tuple[pygame.Surface, Tuple[int, int]]],
    ]:
        output: Dict[
            Tuple[Optional[IntEnum], ...],
            List[Tuple[pygame.Surface, Tuple[int, int]]],
        ] = {}
        assert len(meta) == len(frames)

        enum_permutations = self._enum_permutator(meta)

        for perm in enum_permutations:
            keylist: List[Optional[IntEnum]] = []
            perm_animation_lengths = []
            combined_frames: List[Tuple[pygame.Surface, Tuple[int, int]]] = []

            for enum_id in range(len(perm)):
                enum, w, h = meta[enum_id]
                enum_val = perm[enum_id]

                if enum_val != 0:
                    perm_animation_lengths.append(
                        len(frames[enum_id][enum_val - 1])
                    )
                    keylist.append(enum(enum_val))
                else:
                    perm_animation_lengths.append(1)
                    keylist.append(None)

            lcm = self._lowest_common_multiple_of_list(perm_animation_lengths)

            for frame in range(lcm):
                img_combined = pygame.Surface(size, flags=pygame.SRCALPHA)

                for enum_id in range(len(perm)):
                    enum, w, h = meta[enum_id]
                    offset = w, h

                    if perm[enum_id] == 0:
                        continue

                    anim_frame_num = frame % perm_animation_lengths[enum_id]

                    enum_val = perm[enum_id]
                    enum_frames = frames[enum_id]
                    enum_id_frames = enum_frames[enum_val - 1]

                    surf = enum_id_frames[anim_frame_num]

                    img_combined.blit(surf, offset)
                bounding_rect = img_combined.get_bounding_rect()
                width = bounding_rect.width
                height = bounding_rect.height
                top, left = bounding_rect.topleft
                img_out = pygame.Surface(
                    (width, height), flags=pygame.SRCALPHA
                )
                img_out.blit(img_combined, (-top, -left))

                combined_frames.append((img_out, (top, left)))

            output.update({tuple(keylist): combined_frames})

        return output

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
