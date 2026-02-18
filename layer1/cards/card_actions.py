import random
from typing import Any

import esper

from common import (
    SETTINGS_REF,
    STATE_REF,
    Action,
    ActionArgs,
    Health,
)

from .card_utils import OrganizationEnum
from .cards import DECK_REF, Card
from .log import logger


def play_card(target: ActionArgs) -> None:
    ent = STATE_REF.selected_card

    if ent is None:
        if len(DECK_REF.hand) <= 0:
            return
        ent = DECK_REF.hand[0]

    assert esper.entity_exists(ent)

    card = esper.try_component(ent, Card)
    if card is None:
        return
    if target is not None:
        for effect in card.effects:
            effect(target)

    if STATE_REF.selected_card == ent:
        STATE_REF.selected_card = None
    DECK_REF.hand.remove(ent)
    DECK_REF.discard.append(card)
    esper.component_for_entity(ent, Health).hp = 0


def get_set_order_action(order: OrganizationEnum) -> Action:
    return lambda _: DECK_REF.set_order(order)


def discard_hand(_: ActionArgs) -> None:
    while len(DECK_REF.hand) > 0:
        play_card(None)


def draw_card(_: ActionArgs = None) -> None:
    assert DECK_REF.spawn_card is not None

    if len(DECK_REF.hand) == SETTINGS_REF.MAX_CARD_COUNT:
        logger.info("hand is full")
        return
    if len(DECK_REF.deck) == 0:
        DECK_REF.deck = DECK_REF.discard
        DECK_REF.discard = []
        shuffle_deck()

    if len(DECK_REF.deck) == 0:
        logger.info("out of cards!")
        return

    card = DECK_REF.deck.pop()
    ent = DECK_REF.spawn_card(card)
    DECK_REF.hand.append(ent)
    sort_hand()


def get_draw_cards_action(count: int) -> Action:
    def _draw(__: ActionArgs = None) -> None:
        for _ in range(count):
            draw_card()

    fn = _draw
    return fn


# deck management functions
def sort_hand(_: ActionArgs = None) -> None:
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


def shuffle_deck(_: ActionArgs = None) -> None:
    new = []
    while len(DECK_REF.deck) > 0:
        new.append(
            DECK_REF.deck.pop(
                random.randint(0, len(DECK_REF.deck) - 1),
            )
        )
    DECK_REF.deck = new


STATE_REF.play_card_func = play_card
