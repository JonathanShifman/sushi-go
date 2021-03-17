from players.yoni import YoniUtils, HandEstimation, HandsMemory
from Cards import Cards
from players.yoni.SashimiEvaluation import get_sashimi_value
from players.yoni.DumplingEvaluation import get_dumpling_value
from players.yoni.TempuraEvaluation import get_tempura_value
from players.yoni.NigiriEvaluation import get_nigiri_value
from players.yoni.WasabiEvaluation import get_wasabi_value
from players.yoni.MakiEvaluation import get_maki_value

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
    return -0.1

def get_pudding_value(game_knowledge):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Pudding) is None:
        return -1
    return 1.99

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
        {'type': 'Maki', 'value': get_maki_value(game_knowledge, hand_estimations)},
        {'type': 'Dumpling', 'value': get_dumpling_value(game_knowledge, hand_estimations)},
        {'type': 'Tempura', 'value': get_tempura_value(game_knowledge, hand_estimations)},
        {'type': 'Sashimi', 'value': get_sashimi_value(game_knowledge, hand_estimations)},
        {'type': 'Nigiri', 'value': get_nigiri_value(game_knowledge, hand_estimations)},
        {'type': 'Wasabi', 'value': get_wasabi_value(game_knowledge, hand_estimations)},
    ]

    sorted_card_values = sorted(different_card_values, key=lambda card: card['value'], reverse=True)
    best_value_card = sorted_card_values[0]
    return [get_index_of_best_card(hand, best_value_card['type'])]