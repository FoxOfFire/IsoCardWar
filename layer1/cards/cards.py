import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import esper

from common import Health
from layer1 import MarkerEnum, PriceEnum, set_play_card

from .card_utils import MAX_CARD_COUNT, OrganizationEnum
from .log import logger


# data
@dataclass
class Card:
    name: str
    price: Dict[PriceEnum, int]
    marker: MarkerEnum
    effect: Callable[[int], None]
    current_angle: float
    anim_speed: float
    target_angle: Optional[float] = None


class Deck:
    def __init__(self) -> None:
        self.spawn_card: Optional[Callable[[Card], int]] = None
        self.selected: Optional[int] = None
        self.hand: List[int] = []
        self.deck: List[Card] = _create_starting_deck(20)
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


def get_card_angle(ent: int) -> float:
    card = esper.component_for_entity(ent, Card)
    return card.current_angle


# helper functions
def _create_starting_deck(card_count: int) -> List[Card]:
    cards = []

    def noop(*args: Any) -> None:
        logger.info(f"noop: args({args})")

    for i in range(card_count):
        cards.append(
            Card(
                f"Dummy{i}",
                {PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1},
                MarkerEnum(random.randint(1, 4)),
                noop,
                0,
                20,
            )
        )
    return cards


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


def select_card(ent: int) -> None:
    if ent not in deck_obj.hand or not esper.entity_exists(ent):
        return
    deck_obj.selected = ent


def unselect_card() -> None:
    deck_obj.selected = None
    sort_hand()


def play_card() -> None:
    ent = deck_obj.selected
    if ent is None or not esper.entity_exists(ent):
        return
    card = esper.component_for_entity(ent, Card)
    card.effect(ent)
    deck_obj.selected = None
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
