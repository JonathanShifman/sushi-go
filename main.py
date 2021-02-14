from enum import Enum
import random
import Player

Cards = Enum('Card', 'Nigiri1 Nigiri2 Nigiri3 Wasabi Dumpling Tempura Sashimi Maki1 Maki2 Maki3 Pudding Chopsticks')

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

players = [Player.Player(), Player.Player(), Player.Player(), Player.Player()]
num_of_players = len(players)
cards_per_player = 8

for round_index in range(3):
    hands = []
    for hand_index in range(num_of_players):
        hand = []
        for card_index in range(cards_per_player):
            hand.append(deck[deck_pointer])
            deck_pointer += 1
        hands.append(hand)
    stacks = []
    for stack_index in range(num_of_players):
        stacks.append([])
    while len(hands[0]) > 0:
        for player_index in range(num_of_players):
            chosen_card_index = players[player_index].play()[0]
            stacks[player_index].append(hands[player_index][chosen_card_index])
            del hands[player_index][chosen_card_index]
        temp_hand = hands[num_of_players - 1]
        for hand_index in range(num_of_players - 1, 0, -1):
            hands[hand_index] = hands[hand_index - 1]
        hands[0] = temp_hand
    for stack in stacks:
        print(stack)