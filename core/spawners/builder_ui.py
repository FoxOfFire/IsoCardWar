from enum import IntEnum

import esper

from common import SETTINGS_REF, WORLD_REF
from layer2 import UIElementComponent, UIElemType

from .menu_def import MENU_DEF_REF, MENU_LIST_DEF, MenuContainer
from .spawner_ui import ButtonData, spawn_button


class UIBuilder:
    def _snap(self, snap: IntEnum, size: int, cam_size: int) -> int:
        offset = (snap.value * 2) // cam_size
        ret = snap.value - (offset * size // 2)
        return ret

    def _build_menu(self, menu: MenuContainer) -> UIElementComponent:
        menu_width: int = 0
        menu_height: int = 0
        for button in menu.BUTTONS:
            w, h = 1, 1
            if button is not None and button.size is not None:
                w, h = button.size
            menu_width = max(menu_width, w)
            menu_height += h
        menu_width += menu.edge_padding
        menu_height += menu.edge_padding

        snap_w, snap_h = menu.snap
        x, y = menu.snap_point

        x += self._snap(
            snap_w,
            menu_width * SETTINGS_REF.BUTTON_TILE_SIZE,
            SETTINGS_REF.GAME_CAM_WIDTH,
        )
        y += self._snap(
            snap_h,
            menu_height * SETTINGS_REF.BUTTON_TILE_SIZE,
            SETTINGS_REF.GAME_CAM_HEIGHT,
        )

        menu_ent = spawn_button(
            (x, y),
            ButtonData("", UIElemType.MENU, (menu_width, menu_height)),
        )
        menu_ui_elem = esper.component_for_entity(menu_ent, UIElementComponent)

        w_offset = menu.edge_padding * SETTINGS_REF.BUTTON_TILE_SIZE // 2 + x
        h_offset = menu.edge_padding * SETTINGS_REF.BUTTON_TILE_SIZE // 2 + y
        for button in menu.BUTTONS:
            h = 1
            if button is not None:
                if button.size is None:
                    button.size = (menu_width - menu.edge_padding, 1)
                _, h = button.size
                spawn_button((w_offset, h_offset), button, menu_ui_elem)
            h_offset += (h) * SETTINGS_REF.BUTTON_TILE_SIZE
        return menu_ui_elem

    def build_ui(self) -> None:
        world = WORLD_REF.world
        MENU_LIST_DEF.update({world: []})
        for menu in MENU_DEF_REF[world]:
            MENU_LIST_DEF[world].append(self._build_menu(menu))


UI_BUILDER_REF = UIBuilder()
