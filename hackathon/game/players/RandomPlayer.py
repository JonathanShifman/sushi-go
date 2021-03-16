from evaluations.GameEvaluations import extract_current_plate, extract_current_hand
from evaluations.HandEvaluations import has_chopsticks_in_plate, find_first_chopsticks_index
from players.ProtoPlayer import Player


class RandomPlayer(Player):
    def __init__(self):
        super().__init__('Random Player')

    def play(self, game_knowledge):
        plate_ = extract_current_plate(game_knowledge)
        hand_ = extract_current_hand(game_knowledge)
        if has_chopsticks_in_plate(plate_) and len(hand_) >= 2:
            return [0, 1]
        first_chopsticks_index = find_first_chopsticks_index(hand_)
        if first_chopsticks_index is not None:
            return [first_chopsticks_index]
        return [0]
