from Cards import Cards

def get_name():
    return 'Random Player'

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

def play(game_knowledge):
    if has_chopsticks_in_plate(game_knowledge['currentPlate']) and len(game_knowledge['currentHand']) >= 2:
        return [0, 1]
    first_chopsticks_index = find_first_chopsticks_index(game_knowledge['currentHand'])
    if first_chopsticks_index is not None:
        return [first_chopsticks_index]
    return [0]
