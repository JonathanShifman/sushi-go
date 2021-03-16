from Main import play_single_game
from players.RandomPlayer import RandomPlayer


def test_game_between_two_randoms():
    assert play_single_game(game_name='testGame', players=[RandomPlayer(), RandomPlayer()]) is not None