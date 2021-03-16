from random import random

import pytest

from Cards import Cards
from players.GreedyPlayer import GreedyPlayer
from tests.GameStateBuilder import FillerCardGameBuilder

hand_size = 8
player_knowledge = FillerCardGameBuilder() \
    .set_filler_card(Cards.Maki1) \
    .set_hand_size(8) \
    .build()

game_with_chopsticks_in_plate = player_knowledge.copy()
game_with_chopsticks_in_plate['currentPlate'] = [Cards.Chopsticks]


@pytest.fixture
def first_card_player():
    return GreedyPlayer(lambda _: 0, "null")


@pytest.fixture
def last_card_player():
    global card_viewed
    card_viewed = 0

    def make_last_card_best(card):
        global card_viewed
        card_viewed += 1
        return card_viewed

    return GreedyPlayer(make_last_card_best, "lastCard")


def test_givenHandOfEqualValue_thenGreedyPlayerTakesFirstCard(first_card_player):
    assert first_card_player.play(player_knowledge) == [0]


def test_givenHandOfNonEqualValue_thenGreedyPlayerTakesSingleBestCard():
    global card_viewed, magic_index
    card_viewed = 0
    magic_index = 4

    def make_fourth_card_best(card):
        global card_viewed, magic_index
        value = 1 if card_viewed == magic_index else 0
        card_viewed += 1
        return value

    player = GreedyPlayer(make_fourth_card_best, "magic four")
    assert player.play(player_knowledge) == [magic_index]


def test_whenChopsticksInPlate_thenGreedyPicksTwoCards():
    player = GreedyPlayer(lambda _: random(), "random")
    assert len(player.play(game_with_chopsticks_in_plate)) == 2


def test_bugFix_whenLastCardIsBestAndHadChopsticks_threwException(last_card_player):
    assert len(last_card_player.play(game_with_chopsticks_in_plate)) == 2


def test_bugFix_whenOnlyOneCardRemainedAndHadChopsticks_thenTakenTwoCardsInsteadOfOne(first_card_player):
    game_with_chopsticks_in_plate_and_one_card_in_hand = game_with_chopsticks_in_plate.copy()
    game_with_chopsticks_in_plate_and_one_card_in_hand['currentHand'] = [Cards.Maki1]

    assert len(first_card_player.play(game_with_chopsticks_in_plate_and_one_card_in_hand)) == 1


def test_bugFix_whenUsingChopsticksAndBestCardComesBeforeSecondBest_thenSecondCardIndexWas1LowerThanIntended(
        first_card_player):
    player_move = first_card_player.play(game_with_chopsticks_in_plate)
    assert player_move[0] != 0 or player_move[1] != 0
