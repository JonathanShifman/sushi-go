from Cards import Cards
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
    Cards.Maki1: 0.5,
    Cards.Maki2: 1.5,
    Cards.Maki3: 2.5,
    Cards.Wasabi: 3,
    Cards.Dumpling: 1.5,
}



APRIORY_PLAYER = GreedyPlayer(lambda card: card_apriori_values[card], "April")
