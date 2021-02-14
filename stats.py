class Game:

    def __init__(self):
        self.rounds = []
        self.pudding_scores = None
        self.total_scores = None

    def was_played_by(self, pi):
        return self.total_scores[pi] is not None

    def get_num_of_participating_players(self):
        return len(list(filter(lambda score: score is not None, self.total_scores)))

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

def avg(lst):
    return sum(lst) / len(lst)

def get_stats_for_measure(games, num_of_players, measure):
    return [measure(games, pi) for pi in range(num_of_players)]

def measure_games_played(games, pi):
    return len(list(filter(lambda game: game.total_scores[pi] is not None, games)))

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

def measure_games_placed_first(games, pi):
    return sum([get_first_place_factor(game, pi) for game in games])

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

def measure_games_placed_last(games, pi):
    return sum([get_last_place_factor(game, pi) for game in games])

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

def measure_avg_position_grade(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    return avg([get_position_grade(game, pi) for game in games_played])

def measure_avg_game_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    return avg([game.total_scores[pi] for game in games_played])

def measure_highest_game_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    return max([game.total_scores[pi] for game in games_played])

def measure_lowest_game_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    return min([game.total_scores[pi] for game in games_played])

def measure_avg_round_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    round_scores = []
    for game in games_played:
        round_scores.extend([rnd[pi] for rnd in game.rounds])
    return avg(round_scores)

def measure_highest_round_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    round_scores = []
    for game in games_played:
        round_scores.extend([rnd[pi] for rnd in game.rounds])
    return max(round_scores)

def measure_lowest_round_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    round_scores = []
    for game in games_played:
        round_scores.extend([rnd[pi] for rnd in game.rounds])
    return min(round_scores)

def measure_avg_pudding_score(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    return avg([game.pudding_scores[pi] for game in games_played])

def measure_avg_score_per_card(games, pi):
    games_played = list(filter(lambda game: game.was_played_by(pi), games))
    total_scores = 0
    total_cards = 0
    for game in games_played:
        total_scores += game.total_scores[pi]
        cards_played = 24
        if game.get_num_of_participating_players() == 5:
            cards_played = 21
        total_cards += cards_played
    return total_scores / total_cards

stats = {
    'Games played': get_stats_for_measure(games, num_of_players, measure_games_played),
    'Games placed first': get_stats_for_measure(games, num_of_players, measure_games_placed_first),
    'Games placed last': get_stats_for_measure(games, num_of_players, measure_games_placed_last),
    'Average position grade': get_stats_for_measure(games, num_of_players, measure_avg_position_grade),
    'Average game score': get_stats_for_measure(games, num_of_players, measure_avg_game_score),
    'Highest game score': get_stats_for_measure(games, num_of_players, measure_highest_game_score),
    'Lowest game score': get_stats_for_measure(games, num_of_players, measure_lowest_game_score),
    'Average round score': get_stats_for_measure(games, num_of_players, measure_avg_round_score),
    'Highest round score': get_stats_for_measure(games, num_of_players, measure_highest_round_score),
    'Lowest round score': get_stats_for_measure(games, num_of_players, measure_lowest_round_score),
    'Average pudding score': get_stats_for_measure(games, num_of_players, measure_avg_pudding_score),
    'Average score per card': get_stats_for_measure(games, num_of_players, measure_avg_score_per_card),
}

for key in stats:
    print(key + ': ' + str([round(value, 2) for value in stats[key]]))

separator = ','
output_lines = []
output_lines.append('Stat,' + separator.join(names) + '\n')
for key in stats:
    output_line = key + separator + separator.join([str(round(value, 2)) for value in stats[key]]) + '\n'
    output_lines.append(output_line)

with open('stats.csv', 'w') as f:
    f.writelines(output_lines)
