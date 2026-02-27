from dataclasses import dataclass
from typing import List, Optional, Tuple

from common import Action, TextFunc
from layer2 import UIElemType


@dataclass
class ButtonData:
    text: str | TextFunc
    ui_elem_type: UIElemType
    size: Optional[Tuple[int, int]] = None
    sub_size: Tuple[int, int] = (0, 0)
    click_start_func: Optional[List[Action]] = None
    click_func: Optional[List[Action]] = None
    click_funcing: Optional[List[Action]] = None
    click_cancel_func: Optional[List[Action]] = None
    hover_func: Optional[List[Action]] = None
    start_hover_func: Optional[List[Action]] = None
    remove_hover_func: Optional[List[Action]] = None
    button_default_data: Optional[bool | float] = None
