from Cards import Cards


class FillerCardGameBuilder(object):
    def __init__(self):
        self.playerAmount = 2
        self.cardsInHand = 9
        self.relevant_hand = []
        self.relevant_plate = []
        self.turns_per_round = 9
        self.past_turns = 0
        self.filler_card = Cards.Chopsticks

    def set_player_amount(self, amount: int):
        self.playerAmount = amount
        return self

    def set_hand_size(self, hand_size: int):
        self.cardsInHand = hand_size
        return self

    def set_filler_card(self, filler: Cards):
        self.filler_card = filler
        return self

    def substitute_cards_into_hand(self, cards: list):
        self.relevant_hand = cards
        return self

    def substitute_cards_into_plate(self, cards: list):
        self.relevant_plate = cards
        return self

    def pass_turns(self, turns: int):
        self.past_turns += turns
        return self

    def build(self):
        return {
            'playerIndex': 0,
            'players': [str(i) for i in range(self.playerAmount)],
            'currentHand': self.relevant_hand + [self.filler_card] * (self.cardsInHand - len(self.relevant_hand)),
            'currentPlate': self.relevant_plate + [self.filler_card] * self.past_turns,
            'rounds': [
                {'plates': [[self.filler_card] * self.past_turns] * self.playerAmount}
            ]
        }
