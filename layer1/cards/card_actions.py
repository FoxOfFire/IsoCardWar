import random
from typing import Any, Optional

import esper

from common import (
    SETTINGS_REF,
    STATE_REF,
    Action,
    ActionDecor,
    ActionEnt,
    Health,
)

from .card_utils import OrganizationEnum
from .cards import DECK_REF, Card
from .log import logger


@ActionDecor
def play_card(target: ActionEnt) -> bool:
    ent = STATE_REF.selected_card
    card: Optional[Card] = None

    if ent is None:
        if len(DECK_REF.hand) <= 0:
            return False
        card = DECK_REF.hand[0]
        for search_ent, search_card in esper.get_component(Card):
            if search_card == card:
                ent = search_ent
                logger.info("break")
                break
        if ent is None:
            return False
    else:
        card = esper.try_component(ent, Card)
        if card is None:
            return False
    if target is not None:
        for price in card.price:
            if STATE_REF.resources[price] < card.price[price]:
                return False
        for effect in card.effects:
            if not effect(target, True):
                return False
        for price in card.price:
            STATE_REF.resources[price] -= card.price[price]

    if STATE_REF.selected_card == ent:
        STATE_REF.selected_card = None
    DECK_REF.hand.remove(card)
    DECK_REF.discard.append(card)
    esper.component_for_entity(ent, Health).hp = 0
    return True


def get_set_order_action(order: OrganizationEnum) -> Action:
    return ActionDecor(lambda _: DECK_REF.set_order(order))


@ActionDecor
def discard_hand(_: ActionEnt) -> bool:
    trig = True
    while len(DECK_REF.hand) > 0:
        trig = play_card(None, trig)
    return trig


@ActionDecor
def draw_card(ent: ActionEnt) -> bool:
    if DECK_REF.spawn_card is None:
        return False

    if len(DECK_REF.hand) == SETTINGS_REF.MAX_CARD_COUNT:
        logger.info("hand is full")
        return False
    if len(DECK_REF.deck) == 0:
        DECK_REF.deck = DECK_REF.discard
        DECK_REF.discard = []
        if not shuffle_deck(ent, True):
            return False

    if len(DECK_REF.deck) == 0:
        logger.info("out of cards!")
        return False

    card = DECK_REF.deck.pop()
    card_ent = DECK_REF.spawn_card(card)
    DECK_REF.hand.append(card)
    logger.info(f"Spawned Card {card.name, card_ent}")
    return sort_hand(None, True)


def get_draw_cards_action(count: int) -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        trig = True
        for _ in range(count):
            draw_card(ent, trig)
        return trig

    return action


# deck management functions
@ActionDecor
def sort_hand(_: ActionEnt = None) -> bool:

    def sorter(card: Card) -> Any:
        match DECK_REF.order:
            case OrganizationEnum.NAME:
                return card.name
            case OrganizationEnum.NONE:
                return 0
            case _:
                raise RuntimeError("unexpected organizer")

    DECK_REF.hand.sort(key=sorter)
    return True


@ActionDecor
def shuffle_deck(_: ActionEnt = None) -> bool:
    new = []
    while len(DECK_REF.deck) > 0:
        new.append(
            DECK_REF.deck.pop(
                random.randint(0, len(DECK_REF.deck) - 1),
            )
        )
    DECK_REF.deck = new
    return True


STATE_REF.play_card_func = play_card
