from collections.abc import Callable
from dataclasses import dataclass
from typing import Dict, List, Optional

from common import (
    SETTINGS_REF,
    Action,
    MarkerEnum,
    PriceEnum,
)

from .card_utils import CardTypeEnum, OrganizationEnum
from .log import logger

# data


@dataclass()
class Card:
    name: str
    description: str
    price: Dict[PriceEnum, int]
    marker: MarkerEnum
    effects: List[Action]


class Deck:
    def __init__(self) -> None:
        self.spawn_card: Optional[Callable[[Card], int]] = None
        self.create_card: Optional[Callable[[CardTypeEnum], Card]] = None
        self.hand: List[int] = []
        self.deck: List[Card] = []
        self.discard: List[Card] = []
        self.order: OrganizationEnum = OrganizationEnum.MARKER

    def set_order(self, order: OrganizationEnum) -> None:
        self.order = order

    # card positioning functions
    def get_card_center_offset(self, ent: int) -> float:
        if ent not in self.hand:
            return -1
        hand_size = len(self.hand)
        index = self.hand.index(ent)

        return (hand_size - 1) / 2 - index

    # helper functions
    def create_starting_deck(self) -> None:

        logger.info("creating starting deck")
        cards = []
        if self.create_card is None:
            raise RuntimeError("create_card undefined")

        for _ in range(SETTINGS_REF.STARTER_DECK_COUNT // 3):
            cards.append(self.create_card(CardTypeEnum.DRAW_ONE))
            cards.append(self.create_card(CardTypeEnum.CHANGE_UNIT_AND_DRAW))
            cards.append(
                self.create_card(CardTypeEnum.CHANGE_TERRAIN_AND_DRAW)
            )

        self.deck = cards

    def add_card(self, card: Card) -> None:
        logger.info(f"adding card {card}")
        self.deck.append(card)


# module shenanigans
DECK_REF: Deck = Deck()
