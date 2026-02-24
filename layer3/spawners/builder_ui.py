from enum import IntEnum

import esper

from common import SETTINGS_REF, WORLD_REF
from layer2 import UIElementComponent, UIElemType
from layer3.menu_def import MENU_DEF_REF, MENU_LIST_DEF, MenuContainer

from .spawner_ui import ButtonData, spawn_button


class UIBuilder:
    def _snap(self, snap: IntEnum, size: int, cam_size: int) -> int:
        offset = (snap.value * 2) // cam_size
        ret = snap.value - (offset * size // 2)
        return ret

    def _build_menu(self, menu: MenuContainer) -> UIElementComponent:
        menu_width: int = 0
        menu_height: int = 0
        menu_sub_height: int = 0
        menu_sub_width: int = 0
        for button in menu.BUTTONS:
            w, h = 0, 0
            s_w, s_h = 0, 0
            if not isinstance(button, ButtonData):
                s_w, s_h = button
            elif button.size is not None:
                w, h = button.size
                s_w, s_h = button.sub_size
            else:
                w, h = 1, 1
                s_w, s_h = button.sub_size

            if menu.align_horizontal:
                menu_width += w
                menu_height = max(menu_height, h)
            else:
                menu_width = max(menu_width, w)
                menu_height += h

            menu_sub_width += s_w
            menu_sub_height += s_h
        menu_sub_width += menu.edge_padding * 2
        menu_sub_height += menu.edge_padding * 2

        while menu_sub_width > SETTINGS_REF.BUTTON_TILE_SIZE:
            menu_width += 1
            menu_sub_width -= SETTINGS_REF.BUTTON_TILE_SIZE

        while menu_sub_height > SETTINGS_REF.BUTTON_TILE_SIZE:
            menu_height += 1
            menu_sub_height -= SETTINGS_REF.BUTTON_TILE_SIZE

        snap_w, snap_h = menu.snap
        x, y = menu.snap_point

        x += self._snap(
            snap_w,
            menu_width * SETTINGS_REF.BUTTON_TILE_SIZE + menu_sub_width,
            SETTINGS_REF.GAME_CAM_WIDTH,
        )
        y += self._snap(
            snap_h,
            menu_height * SETTINGS_REF.BUTTON_TILE_SIZE + menu_sub_height,
            SETTINGS_REF.GAME_CAM_HEIGHT,
        )

        menu_ent = spawn_button(
            (x, y),
            ButtonData(
                "",
                UIElemType.MENU,
                (menu_width, menu_height),
                (menu_sub_width, menu_sub_height),
            ),
        )
        menu_ui_elem = esper.component_for_entity(menu_ent, UIElementComponent)

        w_offset = menu.edge_padding + x
        h_offset = menu.edge_padding + y
        for button in menu.BUTTONS:
            h = 0
            w = 0
            s_h = 0
            s_w = 0
            if isinstance(button, ButtonData):
                s_w, s_h = button.sub_size
                if button.size is None:
                    if menu.align_horizontal:
                        button.size = (1, menu_height)
                    else:
                        button.size = (menu_width, 1)
                w, h = button.size
                spawn_button((w_offset, h_offset), button, menu_ui_elem)
            else:
                s_w, s_h = button
            if menu.align_horizontal:
                w_offset += w * SETTINGS_REF.BUTTON_TILE_SIZE + s_w
            else:
                h_offset += h * SETTINGS_REF.BUTTON_TILE_SIZE + s_h
        return menu_ui_elem

    def build_ui(self) -> None:
        world = WORLD_REF.world
        MENU_LIST_DEF.update({world: []})
        for menu in MENU_DEF_REF[world]:
            MENU_LIST_DEF[world].append(self._build_menu(menu))


UI_BUILDER_REF = UIBuilder()
