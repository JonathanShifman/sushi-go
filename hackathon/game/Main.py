import RandomPlayer
from Cards import Cards
import Scoring
import Logging
import KnowledgeFilter
from Deck import Deck
import json

should_load_deck_from_input = False

def load_deck_from_file():
    with open('input/deck.txt', 'r') as f:
        deck_lines = f.readlines()
    cards = [Logging.name_to_card(deck_line.strip()) for deck_line in deck_lines]
    return Deck(cards)


def write_deck_to_file(deck):
    lines = [Logging.card_to_name(card) + '\n' for card in deck.cards]
    with open('output/deck.txt', 'w') as f:
        f.writelines(lines)


def create_deck(should_load_from_input):
    if should_load_from_input:
        return load_deck_from_file()
    deck = Deck()
    write_deck_to_file(deck)
    return deck


def draw_hands(deck, num_of_players):
    hands = []
    for hand_index in range(num_of_players):
        hand = []
        for card_index in range(cards_per_player):
            hand.append(deck.draw_card())
        hands.append(hand)
    return hands

def rotate_hands(hands):
    return [hands[i-1] for i in range(len(hands))]


def is_chosen_card_index_within_hand(chosen_card_index, hand):
    return 0 <= chosen_card_index < len(hand)


def find_chopsticks_index(plate):
    for card_index in range(len(plate)):
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

deck = create_deck(should_load_deck_from_input)
players = [RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer]
num_of_players = len(players)
cards_per_player = 12 - num_of_players
total_scores = [0 for i in range(num_of_players)]
total_pudding_counts = [0 for i in range(num_of_players)]

game_history = {'players': [player.get_name() for player in players], 'rounds': []}

for round_index in range(3):
    round_moves_history = []
    round_history = {
        'roundMoves': round_moves_history
    }
    game_history['rounds'].append(round_history)

    hands = draw_hands(deck, num_of_players)
    plates = [[] for i in range(num_of_players)]
    while len(hands[0]) > 0:
        move_history = []
        for player_index in range(num_of_players):
            player_move_history = {}
            player = players[player_index]
            hand = hands[player_index]
            plate = plates[player_index]
            player_move_history['beforeAction'] = {
                'hand': Logging.cards_to_names(hand),
                'plate': Logging.cards_to_names(plate),
            }
            chosen_card_indices = player.play(KnowledgeFilter.filter_game_knowledge(game_history, player_index, hand, plate))
            chosen_card_indices = validate_chosen_card_indices(hand, plate, chosen_card_indices)
            player_move_history['chosenCardIndices'] = chosen_card_indices
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
                hand.append(Cards.Chopsticks)
            player_move_history['afterAction'] = {
                'hand': Logging.cards_to_names(hand),
                'plate': Logging.cards_to_names(plate),
            }
            move_history.append(player_move_history)
        hands = rotate_hands(hands)
        round_moves_history.append(move_history)
    round_scores = Scoring.get_player_scores(plates)
    total_scores = [sum(scores) for scores in zip(total_scores, round_scores)]
    round_pudding_counts = Scoring.get_round_pudding_counts(plates)
    total_pudding_counts = [sum(counts) for counts in zip(total_pudding_counts, round_pudding_counts)]
    round_history['roundScores'] = round_scores
    round_history['totalScores'] = total_scores
    round_history['roundPuddingCounts'] = round_pudding_counts
    round_history['totalPuddingCounts'] = total_pudding_counts

pudding_scores = Scoring.get_pudding_scores(total_pudding_counts)
final_scores = [sum(scores) for scores in zip(total_scores, pudding_scores)]
game_history['puddingScores'] = pudding_scores
game_history['finalScores'] = final_scores
Logging.log_game_output(game_history)

json_string = json.dumps(game_history)
with open('output/game.json', 'w') as f:
    f.write(json_string)