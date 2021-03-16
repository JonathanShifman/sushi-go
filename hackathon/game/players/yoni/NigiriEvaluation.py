from players.yoni import YoniUtils
from Cards import Cards


def get_strongest_nigiri(hand):
    nigiri3_count = YoniUtils.count_card_occurrences(hand, Cards.Nigiri3)
    nigiri2_count = YoniUtils.count_card_occurrences(hand, Cards.Nigiri2)
    nigiri1_count = YoniUtils.count_card_occurrences(hand, Cards.Nigiri1)
    if nigiri3_count > 0:
        return 3
    if nigiri2_count > 0:
        return 2
    if nigiri1_count > 0:
        return 1
    return 0

def has_wasabi_waiting(hand):
    wasabi_count = 0
    for card in hand:
        if card == Cards.Wasabi:
            wasabi_count += 1
        if card == Cards.Nigiri1 or card == Cards.Nigiri2 or card == Cards.Nigiri3:
            if wasabi_count > 0:
                wasabi_count -= 1
    return wasabi_count > 0


def get_nigiri_value(game_knowledge, hand_estimation):
    hand = game_knowledge['currentHand']
    plate = game_knowledge['currentPlate']
    if YoniUtils.find_first_card_index(hand, Cards.Nigiri1) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Nigiri2) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Nigiri3) is None:
        return -1

    strongest_nigiri = get_strongest_nigiri(hand)
    has_wasabi = has_wasabi_waiting(plate)

    if has_wasabi:
        strongest_nigiri *= 3

    return strongest_nigiri

