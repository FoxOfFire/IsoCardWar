import random
from typing import Any, Callable, Dict, List, Optional

import esper

from common import Health
from common.constants import MAX_CARD_COUNT
from layer1 import (
    MarkerEnum,
    PriceEnum,
    SelectableObject,
    game_state_obj,
    set_play_card,
)

from .card_utils import CardTypeEnum, OrganizationEnum
from .log import logger

# data


class Card(SelectableObject):
    def __init__(
        self,
        name: str,
        price: Dict[PriceEnum, int],
        marker: MarkerEnum,
        effects: List[Callable[[int, int], None]],
    ):
        self.name = name
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
    if ent not in deck_obj.hand:
        return -1
    hand_size = len(deck_obj.hand)
    index = deck_obj.hand.index(ent)

    return (hand_size - 1) / 2 - index


# helper functions
def create_starting_deck(card_count: int) -> None:
    cards = []
    if deck_obj.create_card is None:
        raise RuntimeError("create_card undefined")

    for _ in range(card_count // 3):
        cards.append(deck_obj.create_card(CardTypeEnum.DRAW_ONE))
        cards.append(deck_obj.create_card(CardTypeEnum.CHANGE_UNIT_AND_DRAW))
        cards.append(deck_obj.create_card(CardTypeEnum.CHANGE_TERRAIN_AND_DRAW))

    deck_obj.deck = cards
    shuffle_deck()


def _check_if_card_can_be_drawn() -> bool:
    if len(deck_obj.hand) == MAX_CARD_COUNT:
        logger.info("hand is full")
        return False
    if len(deck_obj.deck) == 0:
        deck_obj.deck = deck_obj.discard
        deck_obj.discard = []
        shuffle_deck()

    if len(deck_obj.deck) == 0:
        logger.info("out of cards!")
        return False

    return True


# deck management functions
def sort_hand() -> None:
    match deck_obj.order:
        case OrganizationEnum.MARKER:

            def sorter(ent: int) -> Any:
                card = esper.component_for_entity(ent, Card)
                return card.marker.value

            pass
        case OrganizationEnum.NAME:

            def sorter(ent: int) -> Any:
                card = esper.component_for_entity(ent, Card)
                return card.name

        case OrganizationEnum.NONE:

            def sorter(ent: int) -> Any:
                return 1

            pass
        case _:
            RuntimeError("unexpected organizer")

    deck_obj.hand.sort(key=sorter)


def shuffle_deck() -> None:
    new = []
    while len(deck_obj.deck) > 0:
        new.append(
            deck_obj.deck.pop(
                random.randint(0, len(deck_obj.deck) - 1),
            )
        )
    deck_obj.deck = new


def play_card(target: int) -> None:
    ent = game_state_obj.selected

    if ent is None or not esper.entity_exists(ent):
        return
    card = esper.try_component(ent, Card)
    if card is None:
        return
    for effect in card.effects:
        effect(ent, target)
    game_state_obj.selected = None
    deck_obj.hand.remove(ent)
    deck_obj.discard.append(card)
    esper.component_for_entity(ent, Health).hp = 0


def draw_card() -> int:
    if deck_obj.spawn_card is None:
        raise RuntimeError("failed to initialise deck_obj")

    if not _check_if_card_can_be_drawn():
        return -1
    card = deck_obj.deck.pop()
    ent = deck_obj.spawn_card(card)
    deck_obj.hand.append(ent)
    sort_hand()
    return ent


def add_card(card: Card) -> None:
    logger.info(f"adding card {card}")
    deck_obj.deck.append(card)
    shuffle_deck()


# module shenanigans
deck_obj: Deck = Deck()
shuffle_deck()
set_play_card(play_card)
