import YoniUtils
from Cards import Cards
import math

def get_dumpling_value(game_knowledge, hand_estimation):
    hand = game_knowledge['currentHand']
    plate = game_knowledge['currentPlate']
    if YoniUtils.find_first_card_index(hand, Cards.Dumpling) is None:
        return -1

    num_of_cards = len(hand)
    num_of_players = len(game_knowledge['players'])
    my_index = game_knowledge['playerIndex']
    dumplings_on_plate = YoniUtils.count_card_occurrences(plate, Cards.Dumpling)

    future_dumplings = 0
    for move_index in range(num_of_cards):
        current_holder_index = YoniUtils.normalize_index(my_index - move_index, num_of_players)
        estimated_dumplings_in_hand = hand_estimation[current_holder_index][Cards.Dumpling]
        loop_index = math.floor(move_index / num_of_players)
        estimated_dumplings_in_hand -= loop_index
        remaining_cards_ratio = (num_of_cards - move_index) / num_of_cards
        estimated_dumplings_in_hand *= remaining_cards_ratio
        future_dumplings += max(0, estimated_dumplings_in_hand)

    current_dumpling_score = 0
    for i in range(dumplings_on_plate):
        current_dumpling_score += i + 1
    next_dumpling_score = dumplings_on_plate + 1

    dumpling_count = 0
    future_dumpling_score = 0
    while dumpling_count + 1 <= future_dumplings:
        future_dumpling_score += next_dumpling_score
        next_dumpling_score += 1
        dumpling_count += 1
    remainder = future_dumplings - dumpling_count
    future_dumpling_score += remainder * (dumpling_count + 1)
    card_value = future_dumpling_score / future_dumplings
    return card_value

