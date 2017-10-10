from tabulate import tabulate
from pprint import pprint

class DeckAnalysis(object):
    """Analyze how a specific hero performs.
    """

    def __init__(self, games: list, hero: str):
        """Create a new analysis given a list of games and a hero."""
        # Only use games for the hero.
        self.games = filter(lambda x: x.hero == hero, games)
        self.hero = hero

        self.wins = 0
        self.losses = 0
        # Opponent dictionary keyed by opponent hero name, value is a dict of win/loss data.
        self.opponents = {}
        # Card dictionary keyed by card name, value is a dict of win/loss data.
        self.cards = {}
        self.__analyze()

    def __analyze(self):
        """Analyze the game data in the context of the hero."""

        for game in self.games:
            if game.won():
                self.wins += 1
            else:
                self.losses += 1

            # Calculate the deck's win rates against the various opponents.
            # Initialize an opponent dict the first time we encounter a new opponent hero.
            opponent = game.opponent
            self.opponents[opponent] = self.opponents.get(opponent, {'games': 0, 'wins': 0, 'losses': 0})
            self.opponents[opponent]['games'] += 1
            if game.won():
                self.opponents[opponent]['wins'] += 1
            else:
                self.opponents[opponent]['losses'] += 1

            # Calculate the per card win rates against the various opponents.
            # Initialize a card dict the first time we encounter a card.
            for card_name in game.cards():
                self.cards[card_name] = self.cards.get(card_name, {'games': 0, 'wins': 0, 'losses': 0, 'opponents': {}})
                self.cards[card_name]['games'] += 1
                if game.won():
                    self.cards[card_name]['wins'] += 1
                else:
                    self.cards[card_name]['losses'] += 1

                self.cards[card_name]['opponents'][opponent] = self.cards[card_name]['opponents'].get(opponent, {'games': 0, 'wins': 0, 'losses': 0})
                self.cards[card_name]['opponents'][opponent]['games'] += 1
                if game.won():
                    self.cards[card_name]['opponents'][opponent]['wins'] += 1
                else:
                    self.cards[card_name]['opponents'][opponent]['losses'] += 1
                
    def summarize(self):
        """Print a table summarizing the game results.
            Shows the deck's win rates against all classes. Classes are sorted by frequency so the most common
            matchups appear first.
            Shows the per card win rates. The unplayed data shows when a card either sits in your hand unplayed
            or isn't drawn.
        """

        # TODO: Look at making it easy to output tables for reddit.
        # tabulate supports tablefmt="mediawiki"

        # Print the deck's win rates.
        headers = ['opponent', 'games', 'wins', 'losses', 'win %']
        game_count = self.wins + self.losses
        # Tabulate expects a list of lists, where each list represents a row of data.
        table = [['All', game_count, self.wins, self.losses, (self.wins / game_count) * 100]]

        # Sort opponents by frequency.
        opponents_by_frequency = []
        for opponent, result in sorted(self.opponents.items(), key=lambda k_v: k_v[1]['games'], reverse=True):
            # Add a row for this opponent.
            opponents_by_frequency.append(opponent)
            table.append([opponent, result['games'], result['wins'], result['losses'], (result['wins'] / result['games']) * 100])

        print()
        print(tabulate(table, headers=headers, floatfmt='.2f'))

        # Print the card analysis.
        # Precompute the various win percentages.
        for card, card_data in self.cards.items():
            card_data['win percentage'] = (card_data['wins'] / card_data['games']) * 100
            card_data['unplayed wins'] = self.wins - card_data['wins']
            card_data['unplayed losses'] = self.losses - card_data['losses']
            card_data['unplayed percentage'] = (card_data['unplayed wins'] / (card_data['unplayed wins'] + card_data['unplayed losses'])) * 100

            for opponent, opp_data in card_data['opponents'].items():
                opp_data['win percentage'] = (opp_data['wins'] / opp_data['games']) * 100
                opp_data['unplayed wins'] = self.opponents[opponent]['wins'] - opp_data['wins']
                opp_data['unplayed losses'] = self.opponents[opponent]['losses'] - opp_data['losses']
                unplayed_games = opp_data['unplayed wins'] + opp_data['unplayed losses']
                opp_data['unplayed percentage'] = 0 if unplayed_games == 0 else (opp_data['unplayed wins'] / (unplayed_games)) * 100
            
        card_headers = ['card vs. All', 'games', 'wins', 'losses', 'win %', 'unplayed wins', 'unplayed losses', 'unplayed %']
        card_table = []
        # Sort cards by best win percentage.
        cards_by_win_percent = []
        for card, card_data in sorted(self.cards.items(), key=lambda k_v: k_v[1]['win percentage'], reverse=True):
            cards_by_win_percent.append(card)
            card_table.append([card, card_data['games'], card_data['wins'], card_data['losses'], card_data['win percentage'],
                               card_data['unplayed wins'], card_data['unplayed losses'], card_data['unplayed percentage']])

        print()
        print(tabulate(card_table, headers=card_headers, floatfmt='.2f'))

        # Print the card vs. specific opponent analysis, also sorted by opponent frequency.
        # Note that this data really starts to suffer from sparse data.        
        for opponent in opponents_by_frequency:
            card_headers = ['card vs. ' + opponent, 'games', 'wins', 'losses', 'win %', 'unplayed wins', 'unplayed losses', 'unplayed %']
            card_table = []
            for card in cards_by_win_percent:
                # Not every card will have been played against every opponent.
                if not opponent in self.cards[card]['opponents']:
                    continue
                card_opp_data = self.cards[card]['opponents'][opponent]
                if card_opp_data is None:
                    continue
                card_table.append([card, card_opp_data['games'], card_opp_data['wins'], card_opp_data['losses'], card_opp_data['win percentage'],
                                   card_opp_data['unplayed wins'], card_opp_data['unplayed losses'], card_opp_data['unplayed percentage']])
            
            print()
            print(tabulate(card_table, headers=card_headers, floatfmt='.2f'))
