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

def card_to_color(card):
    return {
        Cards.Nigiri1: Fore.YELLOW,
        Cards.Nigiri2: Fore.YELLOW,
        Cards.Nigiri3: Fore.YELLOW,
        Cards.Wasabi: Fore.YELLOW,
        Cards.Dumpling: Fore.BLUE,
        Cards.Tempura: Fore.MAGENTA,
        Cards.Sashimi: Fore.GREEN,
        Cards.Maki1: Fore.RED,
        Cards.Maki2: Fore.RED,
        Cards.Maki3: Fore.RED,
        Cards.Pudding: Fore.LIGHTMAGENTA_EX,
        Cards.Chopsticks: Fore.LIGHTCYAN_EX,
    }[card]

def card_to_str(card):
    return Style.BRIGHT + card_to_color(card) + card_to_name(card) + Fore.RESET + Style.RESET_ALL

def plate_to_str(plate):
    return ', '.join([card_to_str(card) for card in plate])