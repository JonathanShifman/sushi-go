from Cards import Cards
from colorama import Fore, Style

def card_to_name(card):
    return {
        Cards.Nigiri1: 'Nigiri1',
        Cards.Nigiri2: 'Nigiri2',
        Cards.Nigiri3: 'Nigiri3',
        Cards.Wasabi: 'Wasabi',
        Cards.Dumpling: 'Dumpling',
        Cards.Tempura: 'Tempura',
        Cards.Sashimi: 'Sashimi',
        Cards.Maki1: 'Maki1',
        Cards.Maki2: 'Maki2',
        Cards.Maki3: 'Maki3',
        Cards.Pudding: 'Pudding',
        Cards.Chopsticks: 'Chopsticks',
    }[card]

def cards_to_names(cards):
    return [card_to_name(card) for card in cards]

def name_to_card(card_name):
    return {
        'Nigiri1': Cards.Nigiri1,
        'Nigiri2': Cards.Nigiri2,
        'Nigiri3': Cards.Nigiri3,
        'Wasabi': Cards.Wasabi,
        'Dumpling': Cards.Dumpling,
        'Tempura': Cards.Tempura,
        'Sashimi': Cards.Sashimi,
        'Maki1': Cards.Maki1,
        'Maki2': Cards.Maki2,
        'Maki3': Cards.Maki3,
        'Pudding': Cards.Pudding,
        'Chopsticks': Cards.Chopsticks,
    }[card_name]

def names_to_cards(card_names):
    return [name_to_card(card_name) for card_name in card_names]

def card_name_to_color(card_name):
    return {
        'Nigiri1': Fore.YELLOW,
        'Nigiri2': Fore.YELLOW,
        'Nigiri3': Fore.YELLOW,
        'Wasabi': Fore.YELLOW,
        'Dumpling': Fore.BLUE,
        'Tempura': Fore.MAGENTA,
        'Sashimi': Fore.GREEN,
        'Maki1': Fore.RED,
        'Maki2': Fore.RED,
        'Maki3': Fore.RED,
        'Pudding': Fore.LIGHTMAGENTA_EX,
        'Chopsticks': Fore.LIGHTCYAN_EX,
    }[card_name]

def card_name_to_str(card_name):
    return Style.BRIGHT + card_name_to_color(card_name) + card_name + Fore.RESET + Style.RESET_ALL

def plate_to_str(plate):
    return ', '.join([card_name_to_str(card_name) for card_name in plate])

def log_game_output(game_history):
    for round_index in range(len(game_history['rounds'])):
        print('Round ' + str(round_index + 1))
        round_history = game_history['rounds'][round_index]
        last_move = round_history['roundMoves'][-1]
        for player_move in last_move:
            print(plate_to_str(player_move['afterAction']['plate']))
        print('Round Scores: ' + str(round_history['roundScores']))
        print('Current Total Scores: ' + str(round_history['totalScores']))
        print('Round Pudding Counts: ' + str(round_history['roundPuddingCounts']))
        print('Current Total Pudding Counts: ' + str(round_history['totalPuddingCounts']))
        print('---------------------')

    print('Pudding Scores: ' + str(game_history['puddingScores']))
    print('Final Scores: ' + str(game_history['finalScores']))
