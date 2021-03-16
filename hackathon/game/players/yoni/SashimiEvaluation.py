from players.yoni import YoniUtils
from Cards import Cards
import math

def get_sashimi_value(game_knowledge, hand_estimation):
    hand = game_knowledge['currentHand']
    plate = game_knowledge['currentPlate']
    if YoniUtils.find_first_card_index(hand, Cards.Sashimi) is None:
        return -1

    num_of_cards = len(hand)
    num_of_players = len(game_knowledge['players'])
    my_index = game_knowledge['playerIndex']
    sashimis_on_plate = YoniUtils.count_card_occurrences(plate, Cards.Sashimi)

    future_sashimis = 0
    for move_index in range(num_of_cards):
        current_holder_index = YoniUtils.normalize_index(my_index - move_index, num_of_players)
        estimated_sashimis_in_hand = hand_estimation[current_holder_index][Cards.Sashimi]
        loop_index = math.floor(move_index / num_of_players)
        estimated_sashimis_in_hand -= loop_index
        remaining_cards_ratio = (num_of_cards - move_index) / num_of_cards
        estimated_sashimis_in_hand *= remaining_cards_ratio
        future_sashimis += min(1, max(0, estimated_sashimis_in_hand))

    if int(sashimis_on_plate) % 3 == 2:
        return 10

    if int(sashimis_on_plate) % 3 == 1:
        return max(1, future_sashimis / 4) * 5

    return min(1, future_sashimis / 6) * 3.33

