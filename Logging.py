from Cards import Cards
from colorama import Fore, Style

def card_to_str(card):
    string_value = {
        Cards.Nigiri1: Fore.YELLOW + 'Nigiri1',
        Cards.Nigiri2: Fore.YELLOW + 'Nigiri2',
        Cards.Nigiri3: Fore.YELLOW + 'Nigiri3',
        Cards.Wasabi: Fore.YELLOW + 'Wasabi',
        Cards.Dumpling: Fore.BLUE + 'Dumpling',
        Cards.Tempura: Fore.MAGENTA + 'Tempura',
        Cards.Sashimi: Fore.GREEN + 'Sashimi',
        Cards.Maki1: Fore.RED + 'Maki1',
        Cards.Maki2: Fore.RED + 'Maki2',
        Cards.Maki3: Fore.RED + 'Maki3',
        Cards.Pudding: Fore.LIGHTMAGENTA_EX + 'Pudding',
        Cards.Chopsticks: Fore.LIGHTCYAN_EX + 'Chopsticks',
    }[card]
    return Style.BRIGHT + string_value + Fore.RESET + Style.RESET_ALL

def plate_to_str(plate):
    return ', '.join([card_to_str(card) for card in plate])