import enum
import random
from dataclasses import dataclass
from math import sqrt
from typing import Callable, Dict, List, Optional, Type

import esper

from common import BoundingBox

from .log import logger

CARD_WIDTH: float = 31.0
CARD_HEIGHT: float = 44.0
ROOT_TWO: float = sqrt(2.0)


class PriceEnum(enum.StrEnum):
    AMMO = "Ammo"
    METAL = "Metal"
    FOOD = "Food"


@dataclass
class Card:
    name: str
    price: Dict[PriceEnum, int]
    effect: Callable[[], None]


def noop() -> None:
    logger.info("played a card")


def get_card_center_offset(ent: int) -> float:
    hand_size = len(deck_obj.hand)
    index = deck_obj.hand.index(ent)

    return (hand_size - 1) / 2 - index


def _create_starting_deck(card_count: int) -> List[Card]:
    cards = []
    for i in range(card_count):
        cards.append(
            Card(
                f"Dummy{i}",
                {PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1},
                noop,
            )
        )
    return cards


class Deck:
    def __init__(self) -> None:
        self.tracker_tag: Optional[Type] = None
        self.sprite: Optional[Type] = None
        self.deck: List[Card] = _create_starting_deck(10)
        self.hand: List[int] = []
        self.discard: List[Card] = []


deck_obj: Deck = Deck()


def play_card(ent: int) -> None:
    logger.info(f"playing card {ent}")
    deck_obj.hand.remove(ent)
    card = esper.component_for_entity(ent, Card)
    card.effect()
    deck_obj.discard.append(card)


def shuffle_deck() -> None:
    logger.info("shuffling deck")
    new = []
    while len(deck_obj.deck) > 0:
        new.append(
            deck_obj.deck.pop(
                random.randint(0, len(deck_obj.deck) - 1),
            )
        )
    deck_obj.deck = new


def draw_card() -> None:
    logger.info("drawing card")
    if len(deck_obj.deck) == 0:
        deck_obj.deck = deck_obj.discard
        deck_obj.discard = []
        shuffle_deck()
    card = deck_obj.deck.pop()

    if deck_obj.tracker_tag is None or deck_obj.sprite is None:
        raise RuntimeError("failed to initialise deck_obj")
    off_x = 40 * len(deck_obj.hand)
    off_y = 80
    bb = BoundingBox(
        off_x, off_x + CARD_WIDTH * ROOT_TWO, off_y, off_y + CARD_HEIGHT * ROOT_TWO
    )
    logger.info(bb)
    ent = esper.create_entity(card, bb, deck_obj.tracker_tag(), deck_obj.sprite())
    deck_obj.hand.append(ent)


def add_card(card: Card) -> None:
    logger.info(f"adding card {card}")
    deck_obj.deck.append(card)
    shuffle_deck()
