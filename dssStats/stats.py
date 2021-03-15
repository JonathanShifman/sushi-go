class Game:

    def __init__(self):
        self.rounds = []
        self.pudding_scores = None
        self.total_scores = None

    def was_played_by(self, pi):
        return self.total_scores[pi] is not None

    def get_num_of_participating_players(self):
        return len(list(filter(lambda score: score is not None, self.total_scores)))

    def num_of_participating_players_matches(self, num_of_participants):
        return num_of_participants is None or self.get_num_of_participating_players() == num_of_participants

with open('SushiGo.csv', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

def get_scores_from_line(line):
    scores = []
    split_line = line.split(',')
    for score in split_line[1:]:
        if score == 'DNP':
            scores.append(None)
        else:
            scores.append(int(score))
    return scores

names = lines[0].split(',')[1:]
num_of_players = len(names)
lines = lines[1:]
games = []
for i in range(0 ,len(lines), 5):
    game = Game()
    for ri in range(3):
        round_scores = get_scores_from_line(lines[i + ri])
        game.rounds.append(round_scores)
    game.pudding_scores = get_scores_from_line(lines[i + 3])
    game.total_scores = get_scores_from_line(lines[i + 4])
    games.append(game)

def calc_avg(lst):
    if len(lst) == 0:
        return None
    return sum(lst) / len(lst)

def calc_max(lst):
    if len(lst) == 0:
        return None
    return max(lst)

def calc_min(lst):
    if len(lst) == 0:
        return None
    return min(lst)

def calc_round(value, digits):
    if value is None:
        return None
    return round(value, digits)

def get_stats_for_measure(games, num_of_players, measure, num_of_participants):
    return [measure(games, pi, num_of_participants) for pi in range(num_of_players)]

def measure_games_played(games, pi, num_of_participants):
    return len(list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games)))

def get_first_place_factor(game, pi):
    player_total_score = game.total_scores[pi]
    if player_total_score is None:
        return 0
    same_count = 0
    for score in game.total_scores:
        if score is None:
            continue
        if score > player_total_score:
            return 0
        if score == player_total_score:
            same_count += 1
    return 1 / same_count

def measure_games_placed_first(games, pi, num_of_participants):
    return sum([get_first_place_factor(game, pi) for game in filter(lambda game: game.num_of_participating_players_matches(num_of_participants), games)])

def get_last_place_factor(game, pi):
    player_total_score = game.total_scores[pi]
    if player_total_score is None:
        return 0
    same_count = 0
    for score in game.total_scores:
        if score is None:
            continue
        if score < player_total_score:
            return 0
        if score == player_total_score:
            same_count += 1
    return 1 / same_count

def measure_games_placed_last(games, pi, num_of_participants):
    return sum([get_last_place_factor(game, pi) for game in filter(lambda game: game.num_of_participating_players_matches(num_of_participants), games)])

def get_position_grade(game, pi):
    grade_delta_per_place = 1 / (game.get_num_of_participating_players() - 1)
    player_total_score = game.total_scores[pi]
    sorted_total_scores = sorted(filter(lambda score: score is not None, game.total_scores))
    lowest_place = None
    highest_place = None
    for current_place in range(len(sorted_total_scores)):
        score = sorted_total_scores[current_place]
        if score == player_total_score:
            highest_place = current_place
            if lowest_place is None:
                lowest_place = current_place
    lowest_place_grade = lowest_place * grade_delta_per_place
    highest_place_grade = highest_place * grade_delta_per_place
    return (lowest_place_grade + highest_place_grade) / 2

def measure_avg_position_grade(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    return calc_avg([get_position_grade(game, pi) for game in games_played])

def measure_avg_game_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    return calc_avg([game.total_scores[pi] for game in games_played])

def measure_highest_game_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    return calc_max([game.total_scores[pi] for game in games_played])

def measure_lowest_game_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    return calc_min([game.total_scores[pi] for game in games_played])

def measure_avg_round_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    round_scores = []
    for game in games_played:
        round_scores.extend([rnd[pi] for rnd in game.rounds])
    return calc_avg(round_scores)

def measure_highest_round_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    round_scores = []
    for game in games_played:
        round_scores.extend([rnd[pi] for rnd in game.rounds])
    return calc_max(round_scores)

def measure_lowest_round_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    round_scores = []
    for game in games_played:
        round_scores.extend([rnd[pi] for rnd in game.rounds])
    return calc_min(round_scores)

def measure_avg_pudding_score(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    return calc_avg([game.pudding_scores[pi] for game in games_played])

def measure_avg_score_per_card(games, pi, num_of_participants):
    games_played = list(filter(lambda game: game.was_played_by(pi) and game.num_of_participating_players_matches(num_of_participants), games))
    total_scores = 0
    total_cards = 0
    for game in games_played:
        total_scores += game.total_scores[pi]
        cards_per_round = 12 - game.get_num_of_participating_players()
        cards_played_in_game = cards_per_round * 3
        total_cards += cards_played_in_game
    if total_cards == 0:
        return None
    return total_scores / total_cards

num_of_participants = None
stats = {
    'Games played': get_stats_for_measure(games, num_of_players, measure_games_played, num_of_participants),
    'Games placed first': get_stats_for_measure(games, num_of_players, measure_games_placed_first, num_of_participants),
    'Games placed last': get_stats_for_measure(games, num_of_players, measure_games_placed_last, num_of_participants),
    'Average position grade': get_stats_for_measure(games, num_of_players, measure_avg_position_grade, num_of_participants),
    'Average game score': get_stats_for_measure(games, num_of_players, measure_avg_game_score, num_of_participants),
    'Highest game score': get_stats_for_measure(games, num_of_players, measure_highest_game_score, num_of_participants),
    'Lowest game score': get_stats_for_measure(games, num_of_players, measure_lowest_game_score, num_of_participants),
    'Average round score': get_stats_for_measure(games, num_of_players, measure_avg_round_score, num_of_participants),
    'Highest round score': get_stats_for_measure(games, num_of_players, measure_highest_round_score, num_of_participants),
    'Lowest round score': get_stats_for_measure(games, num_of_players, measure_lowest_round_score, num_of_participants),
    'Average pudding score': get_stats_for_measure(games, num_of_players, measure_avg_pudding_score, num_of_participants),
    'Average score per card': get_stats_for_measure(games, num_of_players, measure_avg_score_per_card, num_of_participants),
}

num_of_participants_description_string = 'any number of'
if num_of_participants is not None:
    num_of_participants_description_string = str(num_of_participants)
print('Stats for ' + num_of_participants_description_string + ' players:')
for key in stats:
    print(key + ': ' + str([calc_round(value, 2) for value in stats[key]]))

separator = ','
output_lines = []
output_lines.append('Stat,' + separator.join(names) + '\n')
for key in stats:
    output_line = key + separator + separator.join([str(calc_round(value, 2)) for value in stats[key]]) + '\n'
    output_lines.append(output_line)

with open('stats.csv', 'w') as f:
    f.writelines(output_lines)
