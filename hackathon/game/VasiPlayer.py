from Cards import Cards
import random as r


class GeneticStrategy:

    def __init__(self, seed):
        self.player_vector = {}
        r.seed(seed)
        self.player_vector.update({'Tempura': 35})
        self.player_vector.update({'Sashimi': 40})
        self.player_vector.update({'Dumpling': 15})
        self.player_vector.update({'PickMaki': 20})
        self.player_vector.update({'Maki': 12})
        self.player_vector.update({'Wasabi': 50})
        self.player_vector.update({'Nigiri': 10})
        self.player_vector.update({'Pudding': 18})
        self.player_vector.update({'Chopsticks': 25})
        self.player_vector.update({'PickTwoCards': 40})


class GeneticPlayer:

    def __init__(self, geneticStrategy, id):
        self.id = id
        self.geneticStrategy = geneticStrategy

    def get_name(self):
        return 'Vasi'

    def play(self, game_knowledge):
        cards_values = {}

        for card_index in range(len(game_knowledge.get('currentHand'))):
            cards_values.update({card_index: self.calc_card_value(game_knowledge, card_index)})
        best_card_index = max(cards_values, key=lambda x: cards_values[x])
        return [best_card_index]

    def calc_card_value(self, game_knowledge, card_index):
        open_wasabi_amount = self.calc_open_wasabi_amount(game_knowledge.get('currentPlate'))
        card = game_knowledge.get('currentHand')[card_index]
        left_cards_coefficient = (len(game_knowledge.get('currentHand')) / (12 - len(game_knowledge.get('players'))))
        if card.name == 'Wasabi':
            return self.geneticStrategy.player_vector.get('Wasabi') * left_cards_coefficient * pow(2,
                                                                                                   - open_wasabi_amount)
        if card.name == 'Nigiri1':
            if open_wasabi_amount > 0:
                return self.geneticStrategy.player_vector.get('Nigiri') * 3
            else:
                return self.geneticStrategy.player_vector.get('Nigiri')
        if card.name == 'Nigiri2':
            if open_wasabi_amount > 0:
                return self.geneticStrategy.player_vector.get('Nigiri') * 6
            else:
                return self.geneticStrategy.player_vector.get('Nigiri') * 2
        if card.name == 'Nigiri3':
            if open_wasabi_amount > 0:
                return self.geneticStrategy.player_vector.get('Nigiri') * 9
            else:
                return self.geneticStrategy.player_vector.get('Nigiri') * 3

        if card.name == 'Dumpling':
            dumpling_amount = game_knowledge.get('currentPlate').count(Cards.Dumpling)
            return self.geneticStrategy.player_vector.get('Dumpling') * (1 + 0.5 * dumpling_amount)

        if card.name == 'Tempura':
            tempura_amount = game_knowledge.get('currentPlate').count(Cards.Tempura)
            if tempura_amount % 2 == 1:
                return self.geneticStrategy.player_vector.get('Tempura') * 1.5
            else:
                return self.geneticStrategy.player_vector.get('Tempura') * left_cards_coefficient

        if card.name == 'Sashimi':
            sashimi_amount = game_knowledge.get('currentPlate').count(Cards.Sashimi)
            if sashimi_amount % 3 == 2:
                return self.geneticStrategy.player_vector.get('Sashimi') * 1.5
            if sashimi_amount % 3 == 1:
                return self.geneticStrategy.player_vector.get('Sashimi')
            else:
                return self.geneticStrategy.player_vector.get('Sashimi') * left_cards_coefficient

        if card.name == 'Maki1':
            return self.calc_maki_value(game_knowledge)
        if card.name == 'Maki2':
            return self.calc_maki_value(game_knowledge) * 1.5
        if card.name == 'Maki3':
            return self.calc_maki_value(game_knowledge) * 2

        if card.name == 'Pudding':
            return self.geneticStrategy.player_vector.get('Pudding')

        if card.name == 'Chopsticks':
            return self.geneticStrategy.player_vector.get('Chopsticks') * left_cards_coefficient
        return 0

    def calc_open_wasabi_amount(self, currentPlate):
        open_wasabi_amount = 0
        for card in currentPlate:
            if card.name == 'Wasabi':
                open_wasabi_amount += 1
            if card.name == 'Nigiri1':
                open_wasabi_amount -= 1
            if card.name == 'Nigiri2':
                open_wasabi_amount -= 1
            if card.name == 'Nigiri3':
                open_wasabi_amount -= 1
        return open_wasabi_amount

    def calc_maki_value(self, game_knowledge):
        return self.geneticStrategy.player_vector.get('Maki')
