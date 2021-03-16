from random import random

from Cards import Cards
from Deck import Deck
from players.GreedyPlayer import GreedyPlayer


def create_pesudo_random_hand(hand_size):
    deck = Deck()
    return [deck.draw_card() for i in range(hand_size)]


hand_size = 8
player_knowledge = {
    'currentHand': create_pesudo_random_hand(hand_size),
    'currentPlate': []
}


def test_givenHandOfEqualValue_thenGreedyPlayerTakesFirstCard():
    player = GreedyPlayer(lambda x: 0, "null")
    player_move = player.play(player_knowledge)
    assert player_move == [0]


def test_givenHandOfNonEqualValue_thenGreedyPlayerTakesSingleBestCard():
    global card_viewed, magic_index
    card_viewed = 0

    def make_fourth_card_best(card):
        global card_viewed, magic_index
        magic_index = 4
        value = 1 if card_viewed == magic_index else 0
        card_viewed += 1
        return value

    player = GreedyPlayer(make_fourth_card_best, "magic four")
    assert player.play(player_knowledge) == [magic_index]


def test_whenChopsticksInPlate_thenGreedyPicksTwoCards():
    game_with_chopsticks_in_plate = player_knowledge.copy()
    game_with_chopsticks_in_plate['currentPlate'] = [Cards.Chopsticks]
    player = GreedyPlayer(lambda x: random(), "random")
    assert len(player.play(game_with_chopsticks_in_plate)) == 2
2