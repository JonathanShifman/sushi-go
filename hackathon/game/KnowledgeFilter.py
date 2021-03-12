import Logging

def get_cards_chosen_by_player(player_move_history):
    return Logging.names_to_cards([player_move_history['before']['hand'][chosen_card_index] for chosen_card_index in player_move_history['chosenCardIndices']])

def get_cards_chosen_by_players(move_history):
    return [get_cards_chosen_by_player(player_move_history) for player_move_history in move_history]

def filter_move_knowledge(move_history, player_index):
    return {
        'chosenCards': get_cards_chosen_by_players(move_history),
        'hand': Logging.names_to_cards(move_history[player_index]['before']['hand'])
    }

def filter_moves_knowledge(move_histories, player_index):
    return [filter_move_knowledge(move_history, player_index) for move_history in move_histories]

def filter_round_knowledge(round_history, player_index):
    round_knowledge = {}
    if 'roundScores' in round_history:
        round_knowledge['roundScores'] = round_history['roundScores']
        round_knowledge['totalScores'] = round_history['totalScores']
        round_knowledge['roundPuddingCounts'] = round_history['roundPuddingCounts']
        round_knowledge['totalPuddingCounts'] = round_history['totalPuddingCounts']
    round_knowledge['roundMoves'] = filter_moves_knowledge(round_history['roundMoves'], player_index)
    return round_knowledge

def filter_rounds_knowledge(round_histories, player_index):
    return [filter_round_knowledge(round_history, player_index) for round_history in round_histories]

def filter_game_knowledge(game_history, player_index, current_hand):
    return {
        'players': game_history['players'],
        'currentHand': current_hand,
        'rounds': filter_rounds_knowledge(game_history['rounds'], player_index)
    }