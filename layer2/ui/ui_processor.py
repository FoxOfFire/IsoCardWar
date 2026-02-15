from typing import Any, List, Optional, Tuple, Type

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
    GamePhaseType,
)
from layer2.tags import (
    GameCameraTag,
    MaskedSprite,
    UIElementComponent,
    UIStateEnum,
)

from .log import logger


class UIProcessor(esper.Processor):

    def __init__(self) -> None:
        for ent, bb in esper.get_component(BoundingBox):
            if esper.has_component(ent, GameCameraTag):
                self.cam_bb = bb
                break
        self.clicked: List[int] = []
        self.mouse_bb: Optional[BoundingBox] = None
        self.hover: List[int] = []
        logger.info("init finished")
        self.prev_click = False
        self.left_clicking = False
        self.display_size: Optional[Tuple[int, int]] = None
        self.tracker_tag: Optional[Type] = None

    def set_display_size(self, display_size: Tuple[int, int]) -> None:
        logger.info("set display size:" + str(display_size))
        self.display_size = display_size

    def set_tracker_tag(self, tag: Type) -> None:
        logger.info(f"set display size:{tag}")
        self.tracker_tag = tag

    def __get_mask_component(self, ent: int) -> Optional[MaskedSprite]:
        comp: Any
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, MaskedSprite):
                return comp
        return None

    def __mask_mouse_overlap(self, ent: int) -> bool:
        assert esper.entity_exists(ent)
        assert self.mouse_bb is not None
        mask = self.__get_mask_component(ent)
        if mask is None:
            return True
        if not mask.rect.collidepoint(self.mouse_bb.left, self.mouse_bb.top):
            return False

        points = (
            self.mouse_bb.left - mask.rect.left,
            self.mouse_bb.top - mask.rect.top,
        )

        bit = mask.mask.get_at(points)
        return bit == 1

    def __mouse_overlap(self, ent: int) -> bool:
        assert self.mouse_bb is not None
        assert self.tracker_tag is not None
        if self.__get_mask_component(ent) is not None:
            return self.__mask_mouse_overlap(ent)
        else:
            return ent in POS_PROC_REF.intersect(
                self.mouse_bb, self.tracker_tag
            )

    def clicked_things_stay_clicked(self) -> None:
        assert self.mouse_bb is not None
        for ent in self.clicked:
            if not self.__mouse_overlap(ent):
                self.clicked.remove(ent)
                esper.component_for_entity(ent, UIElementComponent).state = (
                    UIStateEnum.BASE
                )

    def press_button_on_release(self) -> None:
        assert self.mouse_bb is not None

        if self.left_clicking or not self.prev_click:
            return

        for ent in self.clicked:
            tag = esper.component_for_entity(ent, UIElementComponent)
            if not self.__mask_mouse_overlap(ent) or (
                STATE_REF.game_phase != GamePhaseType.PLAYER_ACTION
                and tag.is_gameplay_elem
            ):
                continue

            tag.state = UIStateEnum.BASE
            for func in tag.click_func:
                func(ent)

        self.clicked = []

    def reset_hovered_ent(self) -> None:
        assert self.mouse_bb is not None

        for ent, tag in esper.get_component(UIElementComponent):
            if (
                ent in self.clicked
                or tag.is_active
                or self.__mouse_overlap(ent)
                or ent not in self.hover
            ):
                continue

            tag.state = UIStateEnum.BASE
            self.hover.remove(ent)
            for func in tag.end_hover_func:
                func(None)

    def process(self) -> None:
        assert self.display_size is not None
        assert self.tracker_tag is not None
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_bb = BoundingBox(
            self.mouse_pos[0]
            * (SETTINGS_REF.GAME_CAM_WIDTH / self.display_size[0]),
            self.mouse_pos[0]
            * (SETTINGS_REF.GAME_CAM_WIDTH / self.display_size[0]),
            self.mouse_pos[1]
            * (SETTINGS_REF.GAME_CAM_HEIGHT / self.display_size[1]),
            self.mouse_pos[1]
            * (SETTINGS_REF.GAME_CAM_HEIGHT / self.display_size[1]),
        )
        self.left_clicking, _, _ = pygame.mouse.get_pressed()

        self.clicked_things_stay_clicked()

        self.press_button_on_release()

        self.reset_hovered_ent()

        # exiting clicking if continuing to click
        if self.prev_click and self.left_clicking:
            return
        self.prev_click = self.left_clicking

        # pressing first intersection of mouse
        for ent in POS_PROC_REF.intersect(self.mouse_bb, self.tracker_tag):
            assert esper.entity_exists(ent)
            if ent == self.clicked or not self.__mask_mouse_overlap(ent):
                continue

            ui_tag = esper.try_component(ent, UIElementComponent)
            assert ui_tag is not None
            if not ui_tag.is_visible or not ui_tag.is_clickable:
                continue

            if self.left_clicking:
                ui_tag.state = UIStateEnum.PRESSED
                self.clicked.append(ent)
            elif ent not in self.hover:
                for func in ui_tag.start_hover_func:
                    func(ent)
                ui_tag.state = UIStateEnum.HOVER
                self.hover.append(ent)
            else:
                for func in ui_tag.hover_func:
                    func(ent)


UI_PROC_REF = UIProcessor()
