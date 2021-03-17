from players.yoni import YoniUtils
from Cards import Cards
import math


def count_puddings_on_plate(plate):
    return YoniUtils.count_card_occurrences(plate, Cards.Pudding)

def get_current_pudding_counts(game_knowledge):
    pudding_counts_before_round = [0 for _ in game_knowledge['players']]
    current_round = len(game_knowledge['rounds']) - 1
    if current_round > 0:
        pudding_counts_before_round = game_knowledge['rounds'][current_round - 1]['totalPuddingCounts']
    puddings_on_plates = [count_puddings_on_plate(plate) for plate in game_knowledge['rounds'][-1]['plates']]
    return [pudding_counts_before_round[i] + puddings_on_plates[i] for i in range(len(game_knowledge['players']))]

def calc_remaining_puddings(game_knowledge, pudding_counts, hand_estimations):
    num_of_players = len(game_knowledge['players'])
    used_puddings = sum(pudding_counts)

    puddings_in_hands = 0
    for player_index in range(num_of_players):
        hand_estimation = hand_estimations[player_index]
        puddings_in_hands += hand_estimation[Cards.Pudding]
    puddings_in_deck = 10 - used_puddings - puddings_in_hands
    if puddings_in_deck <= 0:
        return puddings_in_hands

    started_rounds = len(game_knowledge['rounds'])
    future_rounds = 3 - started_rounds
    num_of_players = len(game_knowledge['players'])
    cards_per_player_per_round = 12 - num_of_players
    cards_per_round = num_of_players * cards_per_player_per_round
    cards_in_started_rounds = started_rounds * cards_per_round
    cards_in_future_rounds = future_rounds * cards_per_round
    cards_in_deck = 108 - cards_in_started_rounds
    puddings_per_card_in_deck = puddings_in_deck / cards_in_deck
    puddings_in_future_rounds = cards_in_future_rounds * puddings_per_card_in_deck
    return puddings_in_future_rounds + puddings_in_hands



def calc_puddings_required_to_win(pudding_counts, remaining_puddings, my_index):
    current_highest_count = max(pudding_counts)
    if pudding_counts[my_index] == current_highest_count:
        second_highest = 0
        for player_index in range(len(pudding_counts)):
            if player_index == my_index:
                continue
            second_highest = max(second_highest, pudding_counts[player_index])
        if second_highest + remaining_puddings < current_highest_count:
            return 0
        diff = current_highest_count - second_highest
        remaining_puddings -= diff
        return current_highest_count + math.ceil(remaining_puddings / 2)
    my_puddings = pudding_counts[my_index]
    diff = current_highest_count - my_puddings
    if diff >= remaining_puddings:
        return diff
    remaining_puddings -= diff
    return current_highest_count + math.ceil(remaining_puddings / 2)


def get_pudding_value(game_knowledge, hand_estimations):
    hand = game_knowledge['currentHand']
    if YoniUtils.find_first_card_index(hand, Cards.Pudding) is None:
        return -1

    pudding_counts = get_current_pudding_counts(game_knowledge)
    remaining_puddings = calc_remaining_puddings(game_knowledge, pudding_counts, hand_estimations)
    puddings_required_to_win = calc_puddings_required_to_win(pudding_counts, remaining_puddings, game_knowledge['playerIndex'])
    missing_puddings = puddings_required_to_win - pudding_counts[game_knowledge['playerIndex']]
    if missing_puddings <= 0:
        return 0

    potential_step_ratio1 = min(1.0, 1 / missing_puddings)
    potential_step_ratio2 = min(1.0, 1 / remaining_puddings)
    return (potential_step_ratio1*0.5 + potential_step_ratio2*0.5) * 10
