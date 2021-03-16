import YoniUtils
from Cards import Cards
import math

def get_wasabi_value(game_knowledge, hand_estimation):
    hand = game_knowledge['currentHand']
    plate = game_knowledge['currentPlate']
    if YoniUtils.find_first_card_index(hand, Cards.Wasabi) is None:
        return -1

    num_of_cards = len(hand)
    num_of_players = len(game_knowledge['players'])
    my_index = game_knowledge['playerIndex']
    wasabis_on_plate = YoniUtils.count_card_occurrences(plate, Cards.Wasabi)

    future_nigiri1 = 0
    for move_index in range(1, num_of_cards):
        current_holder_index = YoniUtils.normalize_index(my_index - move_index, num_of_players)
        estimated_nigiri1_in_hand = hand_estimation[current_holder_index][Cards.Nigiri1]
        loop_index = math.floor(move_index / num_of_players)
        estimated_nigiri1_in_hand -= loop_index
        remaining_cards_ratio = (num_of_cards - move_index) / num_of_cards
        estimated_nigiri1_in_hand *= remaining_cards_ratio
        future_nigiri1 += max(0, estimated_nigiri1_in_hand)

    future_nigiri2 = 0
    for move_index in range(1, num_of_cards):
        current_holder_index = YoniUtils.normalize_index(my_index - move_index, num_of_players)
        estimated_nigiri2_in_hand = hand_estimation[current_holder_index][Cards.Nigiri2]
        loop_index = math.floor(move_index / num_of_players)
        estimated_nigiri2_in_hand -= loop_index
        remaining_cards_ratio = (num_of_cards - move_index) / num_of_cards
        estimated_nigiri2_in_hand *= remaining_cards_ratio
        future_nigiri2 += max(0, estimated_nigiri2_in_hand)

    future_nigiri3 = 0
    for move_index in range(1, num_of_cards):
        current_holder_index = YoniUtils.normalize_index(my_index - move_index, num_of_players)
        estimated_nigiri3_in_hand = hand_estimation[current_holder_index][Cards.Nigiri3]
        loop_index = math.floor(move_index / num_of_players)
        estimated_nigiri3_in_hand -= loop_index
        remaining_cards_ratio = (num_of_cards - move_index) / num_of_cards
        estimated_nigiri3_in_hand *= remaining_cards_ratio
        future_nigiri3 += max(0, estimated_nigiri3_in_hand)

    future_nigiri = future_nigiri1 + (2*future_nigiri2) + (3*future_nigiri3)
    future_nigiri /= (wasabis_on_plate + 1)

    return min(1, future_nigiri / 9) * 4.5

