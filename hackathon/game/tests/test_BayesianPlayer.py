import pytest

from Main import play_single_game
from VasiPlayer import GeneticPlayer
from evaluations.GameEvaluations import determine_winner_index, TOTAL_CARDS_IN_DECK
from players.BayesianPlayer import *
from players.BayesianPlayer import chances_of_completing_set, estimate_card_in_other_hands
from players.RandomPlayer import RandomPlayer
from players.yoni import YoniPlayer
from tests.GameStateBuilder import FillerCardGameBuilder


class TestAprioriProbabilities(object):
    @staticmethod
    def test_apriori_values_of_nigiris_equal_their_plain_values():
        assert card_apriori_values[Cards.Nigiri1] == 1
        assert card_apriori_values[Cards.Nigiri2] == 2
        assert card_apriori_values[Cards.Nigiri3] == 3

    @staticmethod
    def test_apriori_values_of_risky_cards_equal_their_average_value_per_card():
        assert card_apriori_values[Cards.Tempura] == 2.5
        assert card_apriori_values[Cards.Sashimi] == 3.3

    @staticmethod
    def test_apriori_value_of_pudding_assumes_victory_with_four_picks():
        assert card_apriori_values[Cards.Pudding] == 3

    @staticmethod
    def test_apriori_value_of_maki_equals_amount_of_maki_minus_half():
        assert card_apriori_values[Cards.Maki1] == 0.4
        assert card_apriori_values[Cards.Maki2] == 1.4
        assert card_apriori_values[Cards.Maki3] == 2.4

    @staticmethod
    def test_apriori_value_of_chopsticks_is_not_high():
        assert card_apriori_values[Cards.Chopsticks] < 2

    @staticmethod
    def test_apriori_value_of_wasabi_assumes_egg_nigiri():
        assert card_apriori_values[Cards.Wasabi] == 3

    @staticmethod
    def test_apriori_value_of_dumpling_assumes_two_will_be_taken():
        assert card_apriori_values[Cards.Dumpling] == 1.5


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
        print('victory ratio was: ' + str(victories))
        assert victories > amount_of_games * 0.9

    @staticmethod
    def test_whenFacedWithAprioriPlayer_DeckAwarePlayerWinsInMajorityOfCases():
        victories = 0
        amount_of_games = 100
        for game_round in range(amount_of_games):
            result = play_single_game('test_april_vs_dexter' + str(game_round), [APRIORY_PLAYER, DECK_AWARE_PLAYER],
                should_load_from_input=False, should_log_results=False)
            victories += 1 if determine_winner_index(result) == 1 else 0
        print('victory ratio was: ' + str(victories))
        assert victories > amount_of_games * 0.75

    @staticmethod
    def test_whenFacedWithYoniPlayer_DeckAwarePlayerWinsInMajorityOfCases():
        victories = 0
        amount_of_games = 100
        for game_round in range(amount_of_games):
            result = play_single_game('test_yoni_vs_dexter' + str(game_round), [YoniPlayer, DECK_AWARE_PLAYER],
                should_load_from_input=False, should_log_results=False)
            victories += 1 if determine_winner_index(result) == 1 else 0
        print('victory ratio was: ' + str(victories))
        assert victories > amount_of_games * 0.5

    @staticmethod
    def test_whenFacedWithVasiPlayer_DeckAwarePlayerWinsInMajorityOfCases():
        victories = 0
        amount_of_games = 100
        for game_round in range(amount_of_games):
            result = play_single_game('test_vasi_vs_dexter' + str(game_round), [GeneticPlayer(), DECK_AWARE_PLAYER],
                should_load_from_input=False, should_log_results=False)
            victories += 1 if determine_winner_index(result) == 1 else 0
        print('victory ratio was: ' + str(victories))
        assert victories > amount_of_games * 0.5


    @staticmethod
    def test_whenFacingAllPlayers_thenDeckAwarePlayerWinsInMajorityOfCases():
        victories = 0
        amount_of_games = 100
        for game_round in range(amount_of_games):
            result = play_single_game('test_vasi_vs_dexter_vs_yoni_vs_randy' + str(game_round), [GeneticPlayer(), DECK_AWARE_PLAYER, YoniPlayer, RandomPlayer()],
                should_load_from_input=False, should_log_results=False)
            victories += 1 if determine_winner_index(result) == 1 else 0
        print('victory ratio was: ' + str(victories))
        assert victories > amount_of_games * 0.5


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

    def test_whenOnlyNigiri1Exists_thenNigiriEstimationIs3AtMost(self):
        game_state = FillerCardGameBuilder() \
            .set_filler_card(Cards.Nigiri1) \
            .pass_turns(1) \
            .build()

        assert calculate_future_nigiri_expectancy(game_state) <= 3

    def test_whenOnlyNigiri2Exists_thenNigiriEstimationIsMoreThan1But2AtMost(self):
        game_state = FillerCardGameBuilder() \
            .set_filler_card(Cards.Nigiri2) \
            .pass_turns(1) \
            .build()

        assert calculate_future_nigiri_expectancy(game_state) <= 6
        assert calculate_future_nigiri_expectancy(game_state) > 3

    def test_whenManyTurnsAreLeft_thenChopsticksArePreferableToNigiri1(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(8) \
            .set_filler_card(Cards.Nigiri1) \
            .substitute_cards_into_hand([Cards.Chopsticks]) \
            .build()

        assert evaluate_chopsticks(game_state) > card_apriori_values[Cards.Nigiri1]

    def test_whenAFewTurnsAreLeft_thenChopsticksAreWorthless(self):
        game_state = FillerCardGameBuilder() \
            .set_player_amount(4) \
            .set_hand_size(3) \
            .set_filler_card(Cards.Nigiri1) \
            .substitute_cards_into_hand([Cards.Chopsticks]) \
            .build()

        assert evaluate_chopsticks(game_state) < card_apriori_values[Cards.Nigiri1]

    def test_whenSeesAbundanceOfDumplings_thenDumplingValueExceedsTempura(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(8) \
            .set_filler_card(Cards.Dumpling) \
            .pass_turns(1) \
            .build()

        assert evaluate_dumplings(game_state) > card_apriori_values[Cards.Tempura]

    def test_dumplingsAreAlwaysPreferrableToNigiri1(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(9) \
            .substitute_cards_into_hand([Cards.Dumpling]) \
            .build()

        assert evaluate_dumplings(game_state) > card_apriori_values[Cards.Nigiri1]


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

    def test_whenNoGoodNigiriInGame_thenAprilWillTakeWasabiButDexterWillPreferTempura(self):
        game_state = FillerCardGameBuilder() \
            .set_filler_card(Cards.Tempura) \
            .substitute_cards_into_hand([Cards.Wasabi]) \
            .pass_turns(1) \
            .build()

        assert 0 in APRIORY_PLAYER.play(game_state)
        assert 0 not in DECK_AWARE_PLAYER.play(game_state)

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

    def test_when2CardsLeftInHand_thenAprilWillTakeChopsticksWhileDexterWillPreferNigiri1(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(2) \
            .set_filler_card(Cards.Nigiri1) \
            .substitute_cards_into_hand([Cards.Chopsticks]) \
            .build()

        assert 0 in APRIORY_PLAYER.play(game_state)
        assert 0 not in DECK_AWARE_PLAYER.play(game_state)

    def test_whenInFirstRoundOfGame_thenWasabiShouldBePreferrableToSashimi(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(9) \
            .set_filler_card(Cards.Chopsticks) \
            .substitute_cards_into_hand([Cards.Wasabi, Cards.Sashimi]) \
            .build()

        assert 0 in DECK_AWARE_PLAYER.play(game_state)

    def test_whenChopsticksOnBoardAndWasabiComboAvailable_thenShouldExecuteWasabiCombo(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(8) \
            .set_filler_card(Cards.Chopsticks) \
            .substitute_cards_into_hand([Cards.Wasabi, Cards.Nigiri1, Cards.Nigiri2, Cards.Nigiri3]) \
            .substitute_cards_into_plate([Cards.Chopsticks]) \
            .build()

        assert DECK_AWARE_PLAYER.play(game_state) == [0, 3]

    def test_whenChopsticksOnBoardAndWasabiComboInConfusingOrder_thenWasabiIsStillTakenBeforeNigiri(self):
        game_state = FillerCardGameBuilder() \
            .set_hand_size(8) \
            .substitute_cards_into_hand([Cards.Nigiri1, Cards.Nigiri2, Cards.Wasabi]) \
            .substitute_cards_into_plate([Cards.Chopsticks]) \
            .build()

        assert DECK_AWARE_PLAYER.play(game_state) == [2, 1]
