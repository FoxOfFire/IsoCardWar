from .state import STATE_REF
from .state_utils import Action, ActionDecor, ActionEnt, PriceEnum, Trigger


def reset_trigger(_: ActionEnt, __: Trigger) -> bool:
    return True


def discard_trigger_effect(action: Action) -> Action:
    def sub_action(ent: ActionEnt, trig: Trigger) -> bool:
        action(ent, trig)
        return trig

    return sub_action


@ActionDecor
def end_player_phase_action(_: ActionEnt = None) -> bool:
    STATE_REF.end_player_phase = True
    return True


@ActionDecor
def play_card(ent: ActionEnt) -> bool:
    if STATE_REF.play_card_func is None:
        return False
    return STATE_REF.play_card_func(ent, True)


@ActionDecor
def select_card(ent: ActionEnt) -> bool:
    STATE_REF.selected_card = ent
    return True


@ActionDecor
def hover(ent: ActionEnt) -> bool:
    STATE_REF.hovered_ent = ent
    return True


@ActionDecor
def select_tile(ent: ActionEnt) -> bool:
    STATE_REF.selected_tile = ent
    return True


def get_select_tile_action(ent: ActionEnt) -> Action:
    return ActionDecor(lambda _: select_tile(ent, True))


def get_gain_resource_action(res: PriceEnum, amount: int) -> Action:
    @ActionDecor
    def action(_: ActionEnt) -> bool:
        STATE_REF.resources[res] += amount
        return True

    return action
