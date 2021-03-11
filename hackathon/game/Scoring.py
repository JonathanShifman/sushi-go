from Cards import Cards
import math

def count_card_occurrences(plate, searched_card):
    return len(list(filter(lambda card: card == searched_card, plate)))

def count_makis_in_card(card):
    if card == Cards.Maki1:
        return 1
    if card == Cards.Maki2:
        return 2
    if card == Cards.Maki3:
        return 3
    return 0

def count_makis_in_plate(plate):
    return sum([count_makis_in_card(card) for card in plate])

def get_player_scores_from_maki(plates):
    player_scores = [0 for plate in plates]
    maki_counts = [count_makis_in_plate(plate) for plate in plates]
    maki_winner_count = max(maki_counts)
    num_of_maki_winners = len(list(filter(lambda maki_count: maki_count == maki_winner_count, maki_counts)))
    points_for_maki_winner = math.floor(6 / num_of_maki_winners)
    for i in range(len(maki_counts)):
        if maki_counts[i] == maki_winner_count:
            player_scores[i] = points_for_maki_winner

    if num_of_maki_winners > 1:
        return player_scores
    maki_runner_up_count = max(filter(lambda maki_count: maki_count < maki_winner_count, maki_counts))
    num_of_maki_runners_up = len(list(filter(lambda maki_count: maki_count == maki_runner_up_count, maki_counts)))
    points_for_maki_runner_up = math.floor(3 / num_of_maki_runners_up)
    for i in range(len(maki_counts)):
        if maki_counts[i] == maki_runner_up_count:
            player_scores[i] = points_for_maki_runner_up
    return player_scores



def is_nigiri(card):
    return card == Cards.Nigiri1 or card == Cards.Nigiri2 or card == Cards.Nigiri3

def get_nigiri_value(card):
    if card == Cards.Nigiri1:
        return 1
    if card == Cards.Nigiri2:
        return 2
    if card == Cards.Nigiri3:
        return 3
    return 0

def get_player_score_from_nigiri(plate):
    score = 0
    wasabi_stack_size = 0
    for card in plate:
        if card == Cards.Wasabi:
            wasabi_stack_size += 1
            continue
        if is_nigiri(card):
            card_value = get_nigiri_value(card)
            if wasabi_stack_size > 0:
                card_value *= 3
                wasabi_stack_size -= 1
            score += card_value
    return score


def get_player_scores_from_nigiri(plates):
    return [get_player_score_from_nigiri(plate) for plate in plates]


def get_player_score_from_tempura(plate):
    return math.floor(count_card_occurrences(plate, Cards.Tempura) / 2) * 5

def get_player_score_from_sashimi(plate):
    return math.floor(count_card_occurrences(plate, Cards.Sashimi) / 3) * 10

def get_player_score_from_dumplings(plate):
    remaining_dumplings = count_card_occurrences(plate, Cards.Dumpling)
    score = 0
    while remaining_dumplings >= 5:
        score += 15
        remaining_dumplings -= 5
    for i in range(remaining_dumplings):
        score += i+1
    return score

def get_player_score_from_group_cards(plate):
    return get_player_score_from_tempura(plate) + get_player_score_from_sashimi(plate) + get_player_score_from_dumplings(plate)

def get_player_scores_from_group_cards(plates):
    return [get_player_score_from_group_cards(plate) for plate in plates]


def get_player_scores(plates):
    maki_scores = get_player_scores_from_maki(plates)
    nigiri_scores = get_player_scores_from_nigiri(plates)
    group_card_scores = get_player_scores_from_group_cards(plates)
    return [sum(scores) for scores in zip(maki_scores, nigiri_scores, group_card_scores)]

def get_round_pudding_counts(plates):
    return [count_card_occurrences(plate, Cards.Pudding) for plate in plates]

def get_pudding_scores(pudding_counts):
    pudding_scores = [0 for pudding_count in pudding_counts]
    pudding_winner_count = max(pudding_counts)
    pudding_loser_count = min(pudding_counts)
    num_of_pudding_winners = len(list(filter(lambda pudding_count: pudding_count == pudding_winner_count, pudding_counts)))
    num_of_pudding_losers = len(list(filter(lambda pudding_count: pudding_count == pudding_loser_count, pudding_counts)))
    points_for_pudding_winner = math.floor(6 / num_of_pudding_winners)
    points_for_pudding_loser = -math.floor(6 / num_of_pudding_losers)
    for i in range(len(pudding_counts)):
        if pudding_counts[i] == pudding_winner_count:
            pudding_scores[i] = points_for_pudding_winner
        if pudding_counts[i] == pudding_loser_count:
            pudding_scores[i] = points_for_pudding_loser
    return pudding_scores