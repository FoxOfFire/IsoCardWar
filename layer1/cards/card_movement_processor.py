import esper

from common import BoundingBox

from .cards import Card, deck_obj, get_card_center_offset

from .card_utils import CARD_Y_POS


class CardMovementProcessor(esper.Processor):
    def __init__(self, cam_bb: BoundingBox) -> None:
        self.cam_bb = cam_bb

    def process(self) -> None:
        if len(deck_obj.hand) == 0:
            return

        for ent, _ in esper.get_component(Card):
            bb = esper.component_for_entity(ent, BoundingBox)

            offset = (
                get_card_center_offset(ent)
                * self.cam_bb.width
                / len(deck_obj.hand)
                * 0.8
            )

            if len(deck_obj.hand) < 7:
                offset = get_card_center_offset(ent) * 30

            delta_x = (self.cam_bb.center[0] - bb.center[0] - (offset)) / 20
            bb.delta_right = delta_x
            bb.delta_left = delta_x

            delta_y = (CARD_Y_POS - bb.center[1]) / 20
            bb.delta_top = delta_y
            bb.delta_bottom = delta_y
