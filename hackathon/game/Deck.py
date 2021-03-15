from Cards import Cards
import random

card_quantities = {
    Cards.Nigiri1: 5,
    Cards.Nigiri2: 10,
    Cards.Nigiri3: 5,
    Cards.Wasabi: 6,
    Cards.Dumpling: 14,
    Cards.Tempura: 14,
    Cards.Sashimi: 14,
    Cards.Maki1: 6,
    Cards.Maki2: 12,
    Cards.Maki3: 8,
    Cards.Pudding: 10,
    Cards.Chopsticks: 4,
}

def init_random_deck_cards():
    cards = []
    for card in Cards:
        for i in range(card_quantities[card]):
            cards.append(card)
    random.shuffle(cards)
    return cards

class Deck:

    def __init__(self, cards=None):
        if cards is None:
            self.cards = init_random_deck_cards()
        else:
            self.cards = cards
        self.deck_pointer = 0

    def draw_card(self):
        drawn_card = self.cards[self.deck_pointer]
        self.deck_pointer += 1
        return drawn_card