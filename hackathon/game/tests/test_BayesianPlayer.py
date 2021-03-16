import pytest

from Main import play_single_game
from evaluations.GameEvaluations import determine_winner_index, TOTAL_CARDS_IN_DECK
from players.BayesianPlayer import *
from players.BayesianPlayer import chances_of_completing_set, estimate_card_in_other_hands
from players.RandomPlayer import RandomPlayer
from tests.GameStateBuilder import FillerCardGameBuilder


class TestAprioriProbabilities(object):
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
        assert 0.4 == card_apriori_values[Cards.Maki1]
        assert 1.4 == card_apriori_values[Cards.Maki2]
        assert 2.4 == card_apriori_values[Cards.Maki3]

    @staticmethod
    def test_apriori_value_of_chopsticks_is_nothing():
        assert 0 == card_apriori_values[Cards.Chopsticks]

    @staticmethod
    def test_apriori_value_of_wasabi_assumes_egg_nigiri():
        assert 3 == card_apriori_values[Cards.Wasabi]

    @staticmethod
    def test_apriori_value_of_dumpling_assumes_two_will_be_taken():
        assert 1.5 == card_apriori_values[Cards.Dumpling]


class TestBayesianPlayers(object):

    @staticmethod
    def test_whenFacedWithRandomPlayer_AprioriPlayerWinsInMajorityOfCases():
        random_player = RandomPlayer()
        random_player.name = 'Randy'
        victories = 0
        amount_of_games = 100
        for game_round in range(amount_of_games):
            result = play_single_game('test_april_vs_randy' + str(game_round), [APRIORY_PLAYER, random_player],
                should_load_from_input=False, should_log_results=False)
            victories += 1 if determine_winner_index(result) == 0 else 0
        assert victories > amount_of_games * 0.9

    @staticmethod
    def test_whenFacedWithAprioriPlayer_DeckAwarePlayerWinsInMajorityOfCases():
        victories = 0
        amount_of_games = 100
        for game_round in range(amount_of_games):
            result = play_single_game('test_april_vs_dexter' + str(game_round), [APRIORY_PLAYER, DECK_AWARE_PLAYER],
                should_load_from_input=False, should_log_results=False)
            victories += 1 if determine_winner_index(result) == 1 else 0
        assert victories > amount_of_games * 0.75


class TestBayesianReasoning(object):

    def test_whenNotAwareOfAnySashimis_thenExpectedAmountOfSashimiIsCalculatedRoughly(self):
        hand_size = 9

        game_state = FillerCardGameBuilder() \
            .set_player_amount(2) \
            .set_hand_size(hand_size) \
            .build()

        chance_of_single_sashimi = (card_quantities[Cards.Sashimi] / (TOTAL_CARDS_IN_DECK - hand_size))
        assert estimate_card_in_other_hands(game_state, Cards.Sashimi) == \
               pytest.approx(chance_of_single_sashimi * hand_size)

        game_state = FillerCardGameBuilder() \
            .set_player_amount(4) \
            .set_hand_size(hand_size) \
            .build()

        assert estimate_card_in_other_hands(game_state, Cards.Sashimi) == \
               pytest.approx(chance_of_single_sashimi * hand_size * 3)

    def test_whenAwareOfSashimiInHand_thenEstimatedSashimiAmountIncludesIt(self):
        hand_size = 9

        game_state = FillerCardGameBuilder() \
            .set_player_amount(2) \
            .set_hand_size(hand_size) \
            .substitute_cards_into_hand([Cards.Sashimi]) \
            .build()

        chance_of_single_unseen_sashimi = ((card_quantities[Cards.Sashimi] - 1) / (TOTAL_CARDS_IN_DECK - hand_size))

        assert estimate_card_in_other_hands(game_state, Cards.Sashimi) == \
               pytest.approx(chance_of_single_unseen_sashimi * hand_size)

    def test_whenSashimiExpectancyBelowOne_thenChanceOfCompletingSashimiIs0(self):
        game_state = FillerCardGameBuilder().set_hand_size(2).build()
        assert estimate_card_in_other_hands(game_state, Cards.Sashimi) < 1
        assert chances_of_completing_set(game_state, Cards.Sashimi) == 0

    def test_whenAwareOfAllHandsAndKnowsNotEnoughSashimiAreInPlay_thenChanceOfCompletingSashimiIs0(self):
        hand_size = 9
        game_state = FillerCardGameBuilder() \
            .set_player_amount(2) \
            .set_hand_size(hand_size) \
            .substitute_cards_into_hand([Cards.Sashimi]) \
            .pass_turns(1) \
            .build()

        assert estimate_card_in_other_hands(game_state, Cards.Sashimi) == 0
        assert chances_of_completing_set(game_state, Cards.Sashimi) == 0

    def test_whenHas1SashimiInHandAnd2SashimiOnPlate_thenChanceOfCompletingSashimiIs100(self):
        game_state = FillerCardGameBuilder() \
            .substitute_cards_into_hand([Cards.Sashimi]) \
            .substitute_cards_into_plate([Cards.Sashimi] * 2) \
            .build()

        assert chances_of_completing_set(game_state, Cards.Sashimi) >= 1

    def test_whenHas1SashimiInHandAnd1SashimiOnPlate_thenChanceOfCompletingSashimiIsEstimated(self):
        game_state = FillerCardGameBuilder() \
            .substitute_cards_into_hand([Cards.Sashimi] * 1) \
            .substitute_cards_into_plate([Cards.Sashimi] * 1) \
            .build()

        assert chances_of_completing_set(game_state, Cards.Sashimi) > 0

    def test_whenHas0SashimiInHandAnd2SashimiOnPlate_thenChanceOfCompletingSashimiIsEstimated(self):
        game_state = FillerCardGameBuilder() \
            .substitute_cards_into_plate([Cards.Sashimi] * 2) \
            .build()

        assert chances_of_completing_set(game_state, Cards.Sashimi) > 0

    def test_whenKnowingOfSashimiInOtherPlates_thenSashimiEstimationDecreases(self):
        game_state = FillerCardGameBuilder().set_hand_size(1).build()
        game_state['rounds'] = [{'plates': [[Cards.Sashimi]] * 2}]

        assert count_observed_instances(game_state, Cards.Sashimi) > 0
        assert estimate_card_in_other_hands(game_state, Cards.Sashimi) < card_quantities[
            Cards.Sashimi] / TOTAL_CARDS_IN_DECK


class TestDeckAwareChoices(object):
    def test_whenNotEnoughSashimisInGame_thenAprilWillTakeSashimiButDexterWillNot(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(3) \
            .set_filler_card(Cards.Tempura) \
            .substitute_cards_into_hand([Cards.Sashimi]) \
            .build()

        assert 0 in APRIORY_PLAYER.play(game_state)
        assert 0 not in DECK_AWARE_PLAYER.play(game_state)

    def test_whenNotEnoughTempurasInGame_thenAprilWillTakeTempuraButDexterWillNot(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(3) \
            .set_filler_card(Cards.Nigiri1) \
            .substitute_cards_into_hand([Cards.Tempura]) \
            .build()

        assert 0 in APRIORY_PLAYER.play(game_state)
        assert 0 not in DECK_AWARE_PLAYER.play(game_state)

    # def test_whenNoGoodNigiriInGame_thenAprilWillTakeWasabiButDexterWillNot(self):
    #     game_state = FillerCardGameBuilder() \
    #         .set_filler_card(Cards.Tempura) \
    #         .substitute_cards_into_hand([Cards.Wasabi]) \
    #         .pass_turns(1) \
    #         .build()
    #
    #     assert 0 in APRIORY_PLAYER.play(game_state)
    #     assert 0 not in DECK_AWARE_PLAYER.play(game_state)

    def test_whenTempuraInHandAndOnPlate_thenDexterShouldPreferItToNigiri2(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(2) \
            .set_filler_card(Cards.Nigiri2) \
            .substitute_cards_into_hand([Cards.Tempura]) \
            .substitute_cards_into_plate([Cards.Tempura]) \
            .build()

        assert 0 in DECK_AWARE_PLAYER.play(game_state)

    def test_whenTempuraInHandAndOnPlate_thenDexterShouldPreferItToMaki3(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(2) \
            .substitute_cards_into_hand([Cards.Maki3, Cards.Tempura]) \
            .substitute_cards_into_plate([Cards.Tempura]) \
            .build()

        assert 0 not in DECK_AWARE_PLAYER.play(game_state)
