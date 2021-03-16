import YoniUtils
from Cards import Cards
import math

def get_strongest_maki(hand):
    maki3_count = YoniUtils.count_card_occurrences(hand, Cards.Maki3)
    maki2_count = YoniUtils.count_card_occurrences(hand, Cards.Maki2)
    maki1_count = YoniUtils.count_card_occurrences(hand, Cards.Maki1)
    if maki3_count > 0:
        return 3
    if maki2_count > 0:
        return 2
    if maki1_count > 0:
        return 1
    return 0


def count_makis_on_plate(plate):
    makis_count = 0
    for card in plate:
        if card == Cards.Maki1:
            makis_count += 1
        if card == Cards.Maki2:
            makis_count += 2
        if card == Cards.Maki3:
            makis_count += 3
    return makis_count


def calc_makis_required_to_win(makis_on_plates, remaining_makis, my_index):
    current_highest_plate = max(makis_on_plates)
    if makis_on_plates[my_index] == current_highest_plate:
        second_highest = 0
        for player_index in range(len(makis_on_plates)):
            if player_index == my_index:
                continue
            second_highest = max(second_highest, makis_on_plates[player_index])
        if second_highest + remaining_makis < current_highest_plate:
            return 0
        diff = current_highest_plate - second_highest
        remaining_makis -= diff
        return math.ceil(remaining_makis / 2)
    my_makis = makis_on_plates[my_index]
    diff = current_highest_plate - my_makis
    if diff >= remaining_makis:
        return diff
    remaining_makis -= diff
    return math.ceil(remaining_makis / 2)


def get_maki_value(game_knowledge, hand_estimations):
    hand = game_knowledge['currentHand']
    plate = game_knowledge['currentPlate']
    num_of_players = len(game_knowledge['players'])
    if YoniUtils.find_first_card_index(hand, Cards.Maki1) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Maki2) is None and \
            YoniUtils.find_first_card_index(hand, Cards.Maki3) is None:
        return -1

    strongest_maki = get_strongest_maki(hand)

    total_maki = 0
    for player_index in range(num_of_players):
        hand_estimation = hand_estimations[player_index]
        total_maki += hand_estimation[Cards.Maki1]
        total_maki += hand_estimation[Cards.Maki2] * 2
        total_maki += hand_estimation[Cards.Maki3] * 3

    makis_on_plates = [count_makis_on_plate(plate) for plate in game_knowledge['rounds'][-1]['plates']]
    makis_required_to_win = calc_makis_required_to_win(makis_on_plates, total_maki, game_knowledge['playerIndex'])
    if makis_required_to_win <= 0:
        return 0

    potential_step_ratio = min(1.0, strongest_maki / makis_required_to_win)
    return potential_step_ratio * 4.5
