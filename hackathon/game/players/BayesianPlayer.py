from Cards import Cards
from Deck import card_quantities
from Scoring import count_card_occurrences
from evaluations.CardEvaluations import isCardOfType
from evaluations.GameEvaluations import extract_current_hand, count_unseen_cards_in_deck, count_unseen_cards_in_round, \
    extract_current_plate, count_players, extract_latest_plates
from players.GreedyPlayer import GreedyPlayer


def get_name():
    return 'Naiive Player'


card_apriori_values = {
    Cards.Chopsticks: 0,
    Cards.Nigiri1: 1,
    Cards.Nigiri2: 2,
    Cards.Nigiri3: 3,
    Cards.Tempura: 2.5,
    Cards.Sashimi: 3.3,
    Cards.Pudding: 3,
    Cards.Maki1: 0.4,
    Cards.Maki2: 1.4,
    Cards.Maki3: 2.4,
    Cards.Wasabi: 3,
    Cards.Dumpling: 1.5,
}

APRIORY_PLAYER = GreedyPlayer(lambda card: card_apriori_values[card], "April")

card_scoring_potential = {

}


def count_observed_instances(game_knowledge, desired_card: Cards):
    return sum([isCardOfType(card, desired_card) for card in extract_current_hand(game_knowledge)]) \
           + sum(
        [sum([isCardOfType(card, desired_card) for card in plate]
        ) for plate in extract_latest_plates(game_knowledge)])


def estimate_card_in_other_hands(game_knowledge, desired_card: Cards):
    unseen_cards_in_deck = count_unseen_cards_in_deck(game_knowledge)
    unseen_cards_in_round = count_unseen_cards_in_round(game_knowledge)
    amount_in_hand = count_card_occurrences(extract_current_hand(game_knowledge), desired_card)
    observed_instances = count_observed_instances(game_knowledge, desired_card)
    chance_of_single_appearance = (card_quantities[desired_card] - observed_instances) / unseen_cards_in_deck
    return amount_in_hand - observed_instances \
           + (unseen_cards_in_round * chance_of_single_appearance)


def chances_of_completing_set(game_knowledge, card_of_set: Cards):
    estimation_for_other_hands = estimate_card_in_other_hands(game_knowledge, card_of_set)
    amount_in_hand = count_card_occurrences(extract_current_hand(game_knowledge), card_of_set)
    amount_taken_right_now = (1 if amount_in_hand >= 1 else 0)
    card_set_size = 3 if card_of_set == Cards.Sashimi else 2
    missing_picks = card_set_size \
                    - count_card_occurrences(extract_current_plate(game_knowledge), card_of_set) % card_set_size \
                    - amount_taken_right_now
    future_occurances = (amount_in_hand - amount_taken_right_now) \
                        + estimation_for_other_hands * (0.85 ** (count_players(game_knowledge) - 1))
    return 1 if missing_picks == 0 \
        else 0 if future_occurances < missing_picks \
        else future_occurances / missing_picks


class DeckAwarePlayer(GreedyPlayer):
    def __init__(self):
        super().__init__(lambda _: 0, "Dexter")

    def create_estimation_function(self, turn_state):
        def estimation(card: Cards):
            if card in [Cards.Sashimi, Cards.Tempura]:
                return card_apriori_values[card] * chances_of_completing_set(turn_state, card)
            else:
                return card_apriori_values[card]

        return estimation

    def play(self, game_knowledge):
        self.evaluate = self.create_estimation_function(game_knowledge)
        return super().play(game_knowledge)


DECK_AWARE_PLAYER = DeckAwarePlayer()
