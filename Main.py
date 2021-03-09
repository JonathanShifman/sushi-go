import RandomPlayer
from Cards import Cards
import Scoring
import Logging
from Deck import Deck
import json


def rotate_hands(hands):
    return [hands[i-1] for i in range(len(hands))]


def is_chosen_card_index_within_hand(chosen_card_index, hand):
    return 0 <= chosen_card_index < len(hand)


def find_chopsticks_index(plate):
    for card_index in len(range(plate)):
        if plate[card_index] == Cards.Chopsticks:
            return card_index
    return None


def validate_chosen_card_indices(hand, plate, chosen_card_indices):
    if len(chosen_card_indices) < 1 or len(chosen_card_indices) > 2:
        return [0]
    if len(chosen_card_indices) == 1:
        if is_chosen_card_index_within_hand(chosen_card_indices[0], hand):
            return chosen_card_indices
        return [0]
    if find_chopsticks_index(plate) is not None \
    and is_chosen_card_index_within_hand(chosen_card_indices[0], hand) \
    and is_chosen_card_index_within_hand(chosen_card_indices[1], hand) \
    and chosen_card_indices[0] != chosen_card_indices[1]:
        return chosen_card_indices
    return [0]



print('Starting Game')
print('---------------------')
deck = Deck()
players = [RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer]
num_of_players = len(players)
cards_per_player = 8
total_scores = [0 for i in range(num_of_players)]
total_pudding_counts = [0 for i in range(num_of_players)]

game = {'players': ['Player' for player in players], 'rounds': []}

for round_index in range(3):
    print('Round ' + str(round_index + 1))
    json_round_moves = []
    hands = []
    for hand_index in range(num_of_players):
        hand = []
        for card_index in range(cards_per_player):
            hand.append(deck.draw_card())
        hands.append(hand)
    plates = [[] for i in range(num_of_players)]
    while len(hands[0]) > 0:
        json_player_moves = []
        for player_index in range(num_of_players):
            json_player_move = {}
            player = players[player_index]
            hand = hands[player_index]
            plate = plates[player_index]
            json_player_move['before'] = {
                'hand': Logging.cards_to_names(hand),
                'plate': Logging.cards_to_names(plate),
            }
            chosen_card_indices = player.play(None)
            chosen_card_indices = validate_chosen_card_indices(hand, plate, chosen_card_indices)
            json_player_move['chosenCardIndices'] = chosen_card_indices
            if len(chosen_card_indices) == 1:
                chosen_card_index = chosen_card_indices[0]
                plate.append(hand[chosen_card_index])
                del hand[chosen_card_index]
            else:
                chopsticks_index = find_chopsticks_index(plate)
                del plate[chopsticks_index]
                plate.append(hand[chosen_card_indices[0]])
                plate.append(hand[chosen_card_indices[1]])
                for chosen_card_index in sorted(chosen_card_indices, reverse=True):
                    del hand[chosen_card_index]
            json_player_move['after'] = {
                'hand': Logging.cards_to_names(hand),
                'plate': Logging.cards_to_names(plate),
            }
            json_player_moves.append(json_player_move)
        hands = rotate_hands(hands)
        json_round_moves.append(json_player_moves)
    for plate in plates:
        print(Logging.plate_to_str(plate))
    round_scores = Scoring.get_player_scores(plates)
    print('Round Scores: ' + str(round_scores))
    total_scores = [sum(scores) for scores in zip(total_scores, round_scores)]
    print('Current Total Scores: ' + str(total_scores))
    round_pudding_counts = Scoring.get_round_pudding_counts(plates)
    print('Round Pudding Counts: ' + str(round_pudding_counts))
    total_pudding_counts = [sum(counts) for counts in zip(total_pudding_counts, round_pudding_counts)]
    print('Current Total Pudding Counts: ' + str(total_pudding_counts))
    print('---------------------')
    json_round = {
        'roundMoves': json_round_moves,
        'roundScores': round_scores,
        'totalScores': total_scores,
        'puddingCounts': total_pudding_counts,
    }
    game['rounds'].append(json_round)

pudding_scores = Scoring.get_pudding_scores(total_pudding_counts)
print('Pudding Scores: ' + str(pudding_scores))
total_scores = [sum(scores) for scores in zip(total_scores, pudding_scores)]
print('Final Scores: ' + str(total_scores))
game['puddingScores'] = pudding_scores
game['finalScores'] = total_scores

json_string = json.dumps(game)
with open('output.json', 'w') as f:
    f.write(json_string)