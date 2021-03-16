def find_first_card_index(hand, card):
    for i in range(len(hand)):
        if hand[i] == card:
            return i
    return None

def count_card_occurrences(hand, card):
    cnt = 0
    for i in range(len(hand)):
        if hand[i] == card:
            cnt += 1
    return cnt

def normalize_index(player_index, num_of_players):
    while player_index < 0:
        player_index += num_of_players
    return int(player_index) % int(num_of_players)