from tabulate import tabulate

class DeckAnalysis(object):
    """Analyze how a specific hero performs.
    """

    def __init__(self, games: list, hero: str):
        """Create a new analysis given a list of games and a hero."""
        self.games = games
        self.hero = hero

        self.wins = 0
        self.losses = 0
        self.opponents = {}
        self.__analyze()

    def __analyze(self):
        """Analyze the game data in the context of the hero."""

        for game in self.games:
            if not self.hero == game.hero:
                continue

            if game.won():
                self.wins += 1
            else:
                self.losses += 1

            # Initialize a dict the first time we encounter a new opponent hero.
            opponent = game.opponent
            self.opponents[opponent] = self.opponents.get(opponent, {'games': 0, 'wins': 0, 'losses': 0})
            self.opponents[opponent]['games'] += 1
            if game.won():
                self.opponents[opponent]['wins'] += 1
            else:
                self.opponents[opponent]['losses'] += 1
                
    def summarize(self):
        """Print a table summarizing the game results."""
        headers = ['opponent', 'games', 'wins', 'losses', 'win %']

        # Add the data for the first columns summarizing all games.
        # Tabulate expects a list of lists, where each list represents a row of data.
        game_count = self.wins + self.losses
        table = [['All', game_count, self.wins, self.losses, (self.wins / game_count) * 100]]

        for opponent, result in sorted(self.opponents.items(), key=lambda k_v: k_v[1]['games'], reverse=True):
            # Add a row for this opponent.
            table.append([opponent, result['games'], result['wins'], result['losses'], (result['wins'] / result['games']) * 100])

        print(tabulate(table, headers=headers, floatfmt='.2f'))
