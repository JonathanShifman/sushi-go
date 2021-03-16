import pytest

from evaluations.GameEvaluations import count_seen_hands, count_players, count_cards_seen_in_history, \
    count_unseen_cards_in_round, count_cards_in_hand, count_unseen_hands
from tests.GameStateBuilder import FillerCardGameBuilder


class TestGivenFirstTurnFirstRound(object):
    @pytest.fixture
    def first_turn_state(self):
        return FillerCardGameBuilder().build()

    def test_whenOnFirstTurn_thenSeenOnly1Hand(self, first_turn_state):
        assert count_seen_hands(first_turn_state) == 1

    def test_whenOnFirstTurn_thenHistoryContainsNoCards(self, first_turn_state):
        assert count_cards_seen_in_history(first_turn_state) == 0

    def test_whenOnFirstTurn_thenHasNotSeenHandOfOtherPlayerThisRound(self, first_turn_state):
        assert count_unseen_cards_in_round(first_turn_state) == count_cards_in_hand(first_turn_state)


class TestGivenSecondTurnFirstRound(object):
    @pytest.fixture
    def second_turn_state(self):
        return FillerCardGameBuilder().pass_turns(1).build()

    def test_whenTurnStarts_thenSeenTwoHandsAlready(self, second_turn_state):
        assert count_seen_hands(second_turn_state) == 2


class TestGivenManyRounds(object):
    @pytest.fixture
    def fifth_turn_state(self):
        return FillerCardGameBuilder().pass_turns(5).build()

    def test_whenPassedMoreRoundsThanPlayers_thenSeenAllHands(self, fifth_turn_state):
        assert count_seen_hands(fifth_turn_state) == count_players(fifth_turn_state)
        assert count_unseen_hands(fifth_turn_state) == 0

    def test_whenFiveTurnsPassed_thenHistoryShowsCardPerTurnPerPlayer(self, fifth_turn_state):
        most_updated_plates = fifth_turn_state['rounds'][-1]['plates']
        assert count_cards_seen_in_history(fifth_turn_state) == len(most_updated_plates[0]) * count_players(fifth_turn_state)