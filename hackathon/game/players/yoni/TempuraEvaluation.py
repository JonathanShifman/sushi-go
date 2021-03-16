from players.yoni import YoniUtils
from Cards import Cards
import math

def get_tempura_value(game_knowledge, hand_estimation):
    hand = game_knowledge['currentHand']
    plate = game_knowledge['currentPlate']
    if YoniUtils.find_first_card_index(hand, Cards.Tempura) is None:
        return -1

    num_of_cards = len(hand)
    num_of_players = len(game_knowledge['players'])
    my_index = game_knowledge['playerIndex']
    tempuras_on_plate = YoniUtils.count_card_occurrences(plate, Cards.Tempura)

    future_tempuras = 0
    for move_index in range(num_of_cards):
        current_holder_index = YoniUtils.normalize_index(my_index - move_index, num_of_players)
        estimated_tempuras_in_hand = hand_estimation[current_holder_index][Cards.Tempura]
        loop_index = math.floor(move_index / num_of_players)
        estimated_tempuras_in_hand -= loop_index
        remaining_cards_ratio = (num_of_cards - move_index) / num_of_cards
        estimated_tempuras_in_hand *= remaining_cards_ratio
        future_tempuras += min(1, max(0, estimated_tempuras_in_hand))

    if int(tempuras_on_plate) % 2 == 1:
        return 5

    return min(1, (future_tempuras-1) / 1.5) * 2.5

