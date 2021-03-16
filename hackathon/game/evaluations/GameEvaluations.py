from numpy import argmax


def extract_current_hand(game_knowledge: dict):
    return game_knowledge['currentHand']


def extract_current_plate(game_knowledge: dict):
    return game_knowledge['currentPlate']


def determine_winner_index(final_scores: list):
    return argmax(final_scores)
