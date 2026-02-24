from typing import List

from common import Action, ActionArgs
from layer2 import UIElementComponent


def get_toggle_menu_visibility(
    menus: List[UIElementComponent], menu_num: int
) -> Action:
    def toggle_menu_vis(_: ActionArgs = None) -> None:
        assert menu_num >= 0 and menu_num < len(menus)
        menus[menu_num].is_visible = not menus[menu_num].is_visible

    func = toggle_menu_vis
    return func
