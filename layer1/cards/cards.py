import random
from collections.abc import Callable
from typing import Any, Dict, List, Optional

import esper

from common import MAX_CARD_COUNT, EntityFunc, Health
from layer1.game_state import GAME_STATE_REF, set_play_card
from layer1.game_state_utils import MarkerEnum, PriceEnum, SelectableObject

from .card_utils import CardTypeEnum, OrganizationEnum
from .log import logger

# data


class Card(SelectableObject):
    def __init__(
        self,
        name: str,
        description: str,
        price: Dict[PriceEnum, int],
        marker: MarkerEnum,
        effects: List[EntityFunc],
    ):
        self.name = name
        self.description = description
        self.price = price
        self.marker = marker
        self.effects = effects


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
        sort_hand()


# card positioning functions
def get_card_center_offset(ent: int) -> float:
    if ent not in DECK_REF.hand:
        return -1
    hand_size = len(DECK_REF.hand)
    index = DECK_REF.hand.index(ent)

    return (hand_size - 1) / 2 - index


# helper functions
def create_starting_deck(card_count: int) -> None:
    cards = []
    if DECK_REF.create_card is None:
        raise RuntimeError("create_card undefined")

    for _ in range(card_count // 3):
        cards.append(DECK_REF.create_card(CardTypeEnum.DRAW_ONE))
        cards.append(DECK_REF.create_card(CardTypeEnum.CHANGE_UNIT_AND_DRAW))
        cards.append(DECK_REF.create_card(CardTypeEnum.CHANGE_TERRAIN_AND_DRAW))

    DECK_REF.deck = cards
    shuffle_deck()


def _check_if_card_can_be_drawn() -> bool:
    if len(DECK_REF.hand) == MAX_CARD_COUNT:
        logger.info("hand is full")
        return False
    if len(DECK_REF.deck) == 0:
        DECK_REF.deck = DECK_REF.discard
        DECK_REF.discard = []
        shuffle_deck()

    if len(DECK_REF.deck) == 0:
        logger.info("out of cards!")
        return False

    return True


# deck management functions
def sort_hand() -> None:
    match DECK_REF.order:
        case OrganizationEnum.MARKER:

            def sorter(ent: int) -> Any:
                card = esper.component_for_entity(ent, Card)
                return card.marker.value

        case OrganizationEnum.NAME:

            def sorter(ent: int) -> Any:
                card = esper.component_for_entity(ent, Card)
                return card.name

        case OrganizationEnum.NONE:

            def sorter(ent: int) -> Any:
                return 1

        case _:
            raise RuntimeError("unexpected organizer")

    DECK_REF.hand.sort(key=sorter)


def shuffle_deck() -> None:
    new = []
    while len(DECK_REF.deck) > 0:
        new.append(
            DECK_REF.deck.pop(
                random.randint(0, len(DECK_REF.deck) - 1),
            )
        )
    DECK_REF.deck = new


def play_card(target: Optional[int], card_num: Optional[int]) -> None:
    if card_num is None:
        ent = GAME_STATE_REF.selected
    else:
        assert card_num >= 0 or card_num < len(DECK_REF.hand)
        ent = DECK_REF.hand[card_num]

    if ent is None:
        return

    assert esper.entity_exists(ent)

    card = esper.try_component(ent, Card)
    if card is None:
        return
    if target is not None:
        for effect in card.effects:
            effect(ent, target)

    if GAME_STATE_REF.selected == ent:
        GAME_STATE_REF.selected = None
    DECK_REF.hand.remove(ent)
    DECK_REF.discard.append(card)
    esper.component_for_entity(ent, Health).hp = 0


def discard_card(card_num: int) -> None:
    if card_num < 0 or card_num >= len(DECK_REF.hand):
        return
    ent = DECK_REF.hand[card_num]

    assert esper.entity_exists(ent)
    card = esper.try_component(ent, Card)
    if card is None:
        return
    if GAME_STATE_REF.selected == ent:
        GAME_STATE_REF.selected = None
    DECK_REF.hand.remove(ent)
    DECK_REF.discard.append(card)
    esper.component_for_entity(ent, Health).hp = 0


def draw_card() -> int:
    if DECK_REF.spawn_card is None:
        raise RuntimeError("failed to initialise deck_obj")

    if not _check_if_card_can_be_drawn():
        return -1
    card = DECK_REF.deck.pop()
    ent = DECK_REF.spawn_card(card)
    DECK_REF.hand.append(ent)
    sort_hand()
    return ent


def add_card(card: Card) -> None:
    logger.info(f"adding card {card}")
    DECK_REF.deck.append(card)
    shuffle_deck()


# module shenanigans
DECK_REF: Deck = Deck()
shuffle_deck()
set_play_card(play_card)
