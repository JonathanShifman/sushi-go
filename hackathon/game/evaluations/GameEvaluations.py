from numpy import argmax

from Deck import card_quantities


def extract_current_hand(game_knowledge: dict):
    return game_knowledge['currentHand']


def extract_current_plate(game_knowledge: dict):
    return game_knowledge['currentPlate']


def determine_winner_index(scores_dict: dict):
    return int(argmax(scores_dict['finalScores']))


def count_unseen_cards_in_deck(game_knowledge):
    return TOTAL_CARDS_IN_DECK - \
           (count_cards_in_hand(game_knowledge) * count_seen_hands(game_knowledge)) - \
           count_cards_seen_in_history(game_knowledge)


def count_unseen_cards_in_round(game_knowledge):
    return count_cards_in_hand(game_knowledge) * count_unseen_hands(game_knowledge)


def count_unseen_hands(game_knowledge):
    return count_players(game_knowledge) - count_seen_hands(game_knowledge)


def extract_latest_plates(game_knowledge):
    return game_knowledge['rounds'][-1]['plates']


def count_cards_seen_in_history(game_knowledge):
    return sum(len(plate) for plate in extract_latest_plates(game_knowledge))


def count_seen_hands(game_knowledge):
    return min(
        count_players(game_knowledge),
        1 + count_turns_in_current_round(game_knowledge)
    )


def count_cards_in_hand(game_knowledge):
    return len(extract_current_hand(game_knowledge))


def count_turns_in_current_round(game_knowledge):
    return len(extract_latest_plates(game_knowledge)[-1])


def count_players(game_knowledge):
    return len(game_knowledge['players'])


TOTAL_CARDS_IN_DECK = sum([card_quantities[card] for card in card_quantities.keys()])
