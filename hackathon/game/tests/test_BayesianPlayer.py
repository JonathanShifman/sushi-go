import pytest

from Deck import card_quantities
from Main import play_single_game
from evaluations.CardEvaluations import isCardOfType
from evaluations.GameEvaluations import determine_winner_index, extract_current_hand
from players.BayesianPlayer import *
from players.BayesianPlayer import chances_of_completing_sashimi
from players.RandomPlayer import RandomPlayer
from tests.GameStateBuilder import ChopstickGameBuilder


class TestAprioriProbabilities():
    @staticmethod
    def test_apriori_values_of_nigiris_equal_their_plain_values():
        assert 1 == card_apriori_values[Cards.Nigiri1]
        assert 2 == card_apriori_values[Cards.Nigiri2]
        assert 3 == card_apriori_values[Cards.Nigiri3]

    @staticmethod
    def test_apriori_values_of_risky_cards_equal_their_average_value_per_card():
        assert 2.5 == card_apriori_values[Cards.Tempura]
        assert 3.3 == card_apriori_values[Cards.Sashimi]

    @staticmethod
    def test_apriori_value_of_pudding_assumes_victory_with_four_picks():
        assert 3 == card_apriori_values[Cards.Pudding]

    @staticmethod
    def test_apriori_value_of_maki_equals_amount_of_maki_minus_half():
        assert 0.5 == card_apriori_values[Cards.Maki1]
        assert 1.5 == card_apriori_values[Cards.Maki2]
        assert 2.5 == card_apriori_values[Cards.Maki3]

    @staticmethod
    def test_apriori_value_of_chopsticks_is_nothing():
        assert 0 == card_apriori_values[Cards.Chopsticks]

    @staticmethod
    def test_apriori_value_of_wasabi_assumes_egg_nigiri():
        assert 3 == card_apriori_values[Cards.Wasabi]

    @staticmethod
    def test_apriori_value_of_dumpling_assumes_two_will_be_taken():
        assert 1.5 == card_apriori_values[Cards.Dumpling]


class TestGreedyAprioriPlayer():

    @staticmethod
    def test_whenFacedWithRandomPlayer_AprioriPlayerWins():
        random_player = RandomPlayer()
        random_player.name = 'Randy'
        result = play_single_game('test_april_vs_randy', [APRIORY_PLAYER, random_player])
        assert determine_winner_index(result) == 0

