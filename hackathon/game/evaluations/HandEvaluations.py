from Cards import Cards


def has_chopsticks_in_plate(plate):
    for card in plate:
        if card == Cards.Chopsticks:
            return True
    return False


def find_first_chopsticks_index(hand):
    for i in range(len(hand)):
        if hand[i] == Cards.Chopsticks:
            return i
    return None