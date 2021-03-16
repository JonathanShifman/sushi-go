import YoniUtils
from Cards import Cards
import HandEstimation
import HandsMemory
from SashimiEvaluation import get_sashimi_value
from DumplingEvaluation import get_dumpling_value
from TempuraEvaluation import get_tempura_value

type_to_possible_cards = {
    'Chopsticks': [Cards.Chopsticks],
    'Pudding': [Cards.Pudding],
    'Maki': [Cards.Maki3, Cards.Maki2, Cards.Maki1],
    'Dumpling': [Cards.Dumpling],
    'Tempura': [Cards.Tempura],
    'Sashimi': [Cards.Sashimi],
    'Nigiri': [Cards.Nigiri3, Cards.Nigiri2, Cards.Nigiri1],
    'Wasabi': [Cards.Wasabi],
}

def get_chopsticks_value(game_knowledge):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Chopsticks) is None:
        return -1
    return 0

def get_pudding_value(game_knowledge):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Pudding) is None:
        return -1
    return 1.5

def get_maki_value(game_knowledge):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Maki1) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Maki2) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Maki3) is None:
        return -1
    return 1.5

def get_nigiri_value(game_knowledge):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Nigiri1) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Nigiri2) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Nigiri3) is None:
        return -1
    return 1.5

def get_wasabi_value(game_knowledge):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Wasabi) is None:
        return -1
    return 1.5

def get_index_of_best_card(hand, best_card_type):
    possible_cards = type_to_possible_cards[best_card_type]
    for possible_card in possible_cards:
        card_index = YoniUtils.find_first_card_index(hand, possible_card)
        if card_index is not None:
            return card_index

def play(game_knowledge):
    hand = game_knowledge['currentHand']

    hands_memory = HandsMemory.get_hands_memory(game_knowledge)

    hand_estimations = HandEstimation.estimate_hands(game_knowledge, hands_memory)

    different_card_values = [
        {'type': 'Chopsticks', 'value': get_chopsticks_value(game_knowledge)},
        {'type': 'Pudding', 'value': get_pudding_value(game_knowledge)},
        {'type': 'Maki', 'value': get_maki_value(game_knowledge)},
        {'type': 'Dumpling', 'value': get_dumpling_value(game_knowledge, hand_estimations)},
        {'type': 'Tempura', 'value': get_tempura_value(game_knowledge, hand_estimations)},
        {'type': 'Sashimi', 'value': get_sashimi_value(game_knowledge, hand_estimations)},
        {'type': 'Nigiri', 'value': get_nigiri_value(game_knowledge)},
        {'type': 'Wasabi', 'value': get_wasabi_value(game_knowledge)},
    ]

    sorted_card_values = sorted(different_card_values, key=lambda card: card['value'], reverse=True)
    best_value_card = sorted_card_values[0]
    return [get_index_of_best_card(hand, best_value_card['type'])]