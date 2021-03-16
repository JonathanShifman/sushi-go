from Deck import card_quantities
import YoniUtils

def estimate_statistically(game_knowledge):
    current_hand = game_knowledge['currentHand']
    num_of_cards = len(current_hand)
    num_of_players = len(game_knowledge['players'])
    hand_estimations = []
    remaining_card_quantities = {}
    for card in card_quantities:
        remaining_card_quantities[card] = card_quantities[card]
    for round in game_knowledge['rounds']:
        for plate in round['plates']:
            for card in plate:
                remaining_card_quantities[card] -= 1
    for card in current_hand:
        remaining_card_quantities[card] -= 1
    total_remaining_cards = sum([remaining_card_quantities[card] for card in remaining_card_quantities])

    for player_index in range(num_of_players):
        hand_estimation = {}
        if player_index == game_knowledge['playerIndex']:
            for card in card_quantities:
                hand_estimation[card] = YoniUtils.count_card_occurrences(current_hand, card)
        else:
            for card in card_quantities:
                hand_estimation[card] = (num_of_cards / total_remaining_cards) * remaining_card_quantities[card]
        hand_estimations.append(hand_estimation)
    return hand_estimations

def estimate_by_round_history(game_knowledge):
    pass

def estimate_hands(game_knowledge):
    current_round_index = len(game_knowledge['rounds']) - 1
    current_round = game_knowledge['rounds'][current_round_index]
    current_move_index = len(current_round['roundMoves'])
    return estimate_statistically(game_knowledge)
    # if current_move_index == 0:
    #     return estimate_statistically(game_knowledge)
    # return estimate_by_round_history(game_knowledge)


