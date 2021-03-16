from numpy import argmax

from evaluations.GameEvaluations import extract_current_plate, extract_current_hand
from evaluations.HandEvaluations import has_chopsticks_in_plate


class GreedyPlayer(object):
    def __init__(self, evaluation_function, evaluation_name):
        self.evaluate = evaluation_function
        self.evaluation_name = evaluation_name

    def get_name(self):
        return self.evaluation_name + (' (Greedy Player)')

    def evaluate_hand(self, hand):
        return [self.evaluate(card) for card in hand]

    def play(self, game_knowledge) -> list:
        evaluations_list = self.evaluate_hand(extract_current_hand(game_knowledge))
        best_card_index = int(argmax(evaluations_list))
        if has_chopsticks_in_plate(extract_current_plate(game_knowledge)):
            return [int(argmax(
                evaluations_list[0:best_card_index] + evaluations_list[best_card_index + 1: len(evaluations_list)])
            )] + [best_card_index]
        return [best_card_index]
