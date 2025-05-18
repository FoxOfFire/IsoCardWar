import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type, Unpack

import esper

from common import BoundingBox, Health

from .card_utils import (
    CARD_HEIGHT,
    CARD_START_X,
    CARD_START_Y,
    CARD_WIDTH,
    MAX_CARD_COUNT,
    ROOT_TWO,
    MarkerEnum,
    PriceEnum,
)
from .log import logger


@dataclass
class Card:
    name: str
    price: Dict[PriceEnum, int]
    marker: MarkerEnum
    effect: Callable[[Unpack[Any]], None]
    current_angle: float
    anim_speed: float
    target_angle: Optional[float] = None


def get_card_center_offset(ent: int) -> float:
    if ent not in deck_obj.hand:
        return -1
    hand_size = len(deck_obj.hand)
    index = deck_obj.hand.index(ent)

    return (hand_size - 1) / 2 - index


def get_card_angle(ent: int) -> float:
    card = esper.component_for_entity(ent, Card)
    return card.current_angle


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


def sort_hand() -> None:
    pass


class Deck:
    def __init__(self) -> None:
        self.tracker_tag: Optional[Type] = None
        self.sprite: Optional[Type] = None
        self.ui_tag: Optional[Type] = None
        self.deck: List[Card] = _create_starting_deck(20)
        self.hand: List[int] = []
        self.discard: List[Card] = []


def shuffle_deck() -> None:
    new = []
    while len(deck_obj.deck) > 0:
        new.append(
            deck_obj.deck.pop(
                random.randint(0, len(deck_obj.deck) - 1),
            )
        )
    deck_obj.deck = new


deck_obj: Deck = Deck()
shuffle_deck()


def play_card(ent: int) -> None:
    if ent not in deck_obj.hand:
        return
    deck_obj.hand.remove(ent)
    card = esper.component_for_entity(ent, Card)
    card.effect(card.name, card.marker)
    deck_obj.discard.append(card)
    esper.component_for_entity(ent, Health).hp = 0


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


def _get_new_card_bb() -> BoundingBox:
    bb_size = ROOT_TWO / 2 * (CARD_HEIGHT + CARD_WIDTH)

    width_offset = (bb_size - CARD_WIDTH) / 2
    height_offset = (bb_size - CARD_HEIGHT) / 2

    return BoundingBox(
        CARD_START_X - width_offset,
        CARD_START_X + width_offset + CARD_WIDTH,
        CARD_START_Y - height_offset,
        CARD_START_Y + height_offset + CARD_HEIGHT,
    )


def draw_card() -> int:
    if (
        deck_obj.tracker_tag is None
        or deck_obj.sprite is None
        or deck_obj.ui_tag is None
    ):
        raise RuntimeError("failed to initialise deck_obj")

    if not _check_if_card_can_be_drawn():
        return -1
    bb = _get_new_card_bb()
    card = deck_obj.deck.pop()
    card.current_angle = 0
    card.target_angle = None
    ent = esper.create_entity(
        card, bb, deck_obj.tracker_tag(), deck_obj.sprite(), deck_obj.ui_tag(), Health()
    )
    deck_obj.hand.append(ent)
    return ent


def add_card(card: Card) -> None:
    logger.info(f"adding card {card}")
    deck_obj.deck.append(card)
    shuffle_deck()
