import random
import RandomPlayer
from Cards import Cards
import Scoring
import Logging

card_quantities = {
    Cards.Nigiri1: 5,
    Cards.Nigiri2: 10,
    Cards.Nigiri3: 5,
    Cards.Wasabi: 6,
    Cards.Dumpling: 14,
    Cards.Tempura: 14,
    Cards.Sashimi: 14,
    Cards.Maki1: 6,
    Cards.Maki2: 12,
    Cards.Maki3: 8,
    Cards.Pudding: 10,
    Cards.Chopsticks: 4,
}

deck = []
for card in Cards:
    for i in range(card_quantities[card]):
        deck.append(card)
random.shuffle(deck)
deck_pointer = 0

players = [RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer]
num_of_players = len(players)
cards_per_player = 8

print('Starting Game')
print('---------------------')
total_scores = [0 for i in range(num_of_players)]
total_pudding_counts = [0 for i in range(num_of_players)]
for round_index in range(3):
    print('Round ' + str(round_index + 1))
    hands = []
    for hand_index in range(num_of_players):
        hand = []
        for card_index in range(cards_per_player):
            hand.append(deck[deck_pointer])
            deck_pointer += 1
        hands.append(hand)
    plates = [[] for i in range(num_of_players)]
    while len(hands[0]) > 0:
        for player_index in range(num_of_players):
            chosen_card_index = players[player_index].play(None)[0]
            plates[player_index].append(hands[player_index][chosen_card_index])
            del hands[player_index][chosen_card_index]
        temp_hand = hands[num_of_players - 1]
        for hand_index in range(num_of_players - 1, 0, -1):
            hands[hand_index] = hands[hand_index - 1]
        hands[0] = temp_hand
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

pudding_scores = Scoring.get_pudding_scores(total_pudding_counts)
print('Pudding Scores: ' + str(pudding_scores))
total_scores = [sum(scores) for scores in zip(total_scores, pudding_scores)]
print('Final Scores: ' + str(total_scores))