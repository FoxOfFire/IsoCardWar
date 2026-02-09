import random
from typing import Any, Optional

import esper

from common import GAME_STATE_REF, MAX_CARD_COUNT, Action, ActionDecor, Health

from .card_utils import OrganizationEnum
from .cards import DECK_REF, Card
from .log import logger


@ActionDecor
def play_card(target: Optional[int], card_num: Optional[int]) -> None:
    if card_num is None:
        ent = GAME_STATE_REF.selected
    else:
        if card_num < 0 or card_num >= len(DECK_REF.hand):
            return
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


@ActionDecor
def draw_card(_: Optional[int] = None, __: Optional[int] = None) -> None:
    if DECK_REF.spawn_card is None:
        raise RuntimeError("failed to initialise deck_obj")

    if len(DECK_REF.hand) == MAX_CARD_COUNT:
        logger.info("hand is full")
        return
    if len(DECK_REF.deck) == 0:
        DECK_REF.deck = DECK_REF.discard
        DECK_REF.discard = []
        shuffle_deck(None, None)

    if len(DECK_REF.deck) == 0:
        logger.info("out of cards!")
        return

    card = DECK_REF.deck.pop()
    ent = DECK_REF.spawn_card(card)
    DECK_REF.hand.append(ent)
    sort_hand(None, None)


def draw_cards(count: int) -> Action:
    @ActionDecor
    def _draw(_: Optional[int] = None, __: Optional[int] = None) -> None:
        for _ in range(count):
            draw_card(None, None)

    fn = _draw
    return fn


# deck management functions
@ActionDecor
def sort_hand(_: Optional[int] = None, __: Optional[int] = None) -> None:
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


@ActionDecor
def shuffle_deck(_: Optional[int] = None, __: Optional[int] = None) -> None:
    new = []
    while len(DECK_REF.deck) > 0:
        new.append(
            DECK_REF.deck.pop(
                random.randint(0, len(DECK_REF.deck) - 1),
            )
        )
    DECK_REF.deck = new


GAME_STATE_REF.play_card_func = play_card
