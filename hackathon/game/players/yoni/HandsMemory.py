from players.yoni import YoniUtils
from Cards import Cards


def rotate_hands(hands):
    return [hands[i - 1] for i in range(len(hands))]

def get_hands_memory(game_knowledge):
    num_of_players = len(game_knowledge['players'])
    my_index = game_knowledge['playerIndex']
    hands = [None for _ in range(num_of_players)]
    current_round = game_knowledge['rounds'][-1]
    for move in current_round['roundMoves']:
        hands[my_index] = YoniUtils.copy_list(move['hand'])
        chosen_cards = move['chosenCards']
        for player_index in range(len(chosen_cards)):
            player_chosen_cards = chosen_cards[player_index]
            if hands[player_index] is not None:
                for chosen_card in player_chosen_cards:
                    index_of_card_to_delete = YoniUtils.find_first_card_index(hands[player_index], chosen_card)
                    del hands[player_index][index_of_card_to_delete]
                if len(player_chosen_cards) > 1:
                    hands[player_index].append(Cards.Chopsticks)
        hands = rotate_hands(hands)
    hands[my_index] = YoniUtils.copy_list(game_knowledge['currentHand'])
    return hands
