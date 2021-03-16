from Deck import card_quantities
import YoniUtils

def estimate_hands(game_knowledge, hands_memory):
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
    for hand in hands_memory:
        if hand is not None:
            for card in hand:
                remaining_card_quantities[card] -= 1
    total_remaining_cards = sum([remaining_card_quantities[card] for card in remaining_card_quantities])

    for player_index in range(num_of_players):
        if hands_memory[player_index] is not None:
            hand_estimation = {}
            for card in card_quantities:
                hand_estimation[card] = YoniUtils.count_card_occurrences(hands_memory[player_index], card)
            hand_estimations.append(hand_estimation)
            continue
        hand_estimation = {}
        if player_index == game_knowledge['playerIndex']:
            for card in card_quantities:
                hand_estimation[card] = YoniUtils.count_card_occurrences(current_hand, card)
        else:
            for card in card_quantities:
                hand_estimation[card] = (num_of_cards / total_remaining_cards) * remaining_card_quantities[card]
        hand_estimations.append(hand_estimation)
    return hand_estimations


