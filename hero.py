from tabulate import tabulate
from pprint import pprint

class Hero(object):
    """Analyze how a specific hero performs.
        TODO: Look at making it easy to output tables for reddit.
        tabulate supports tablefmt="mediawiki"
    """

    def __init__(self, games: list, hero: str):
        """Create a new hero given a list of games and a hero."""
        self.games = []
        self.hero = hero
        self.wins = 0
        self.losses = 0

        # Opponent dictionary keyed by opponent hero name, value is a dict of win/loss data.
        self.opponents = {}

        # Perform initial calculations that get used by multiple analyses.
        for game in filter(lambda x: x.hero == hero, games):
            self.games.append(game)
            if game.won():
                self.wins += 1
            else:
                self.losses += 1

            opponent = game.opponent
            self.opponents[opponent] = self.opponents.get(opponent, {'games': 0, 'wins': 0, 'losses': 0})
            self.opponents[opponent]['games'] += 1
            if game.won():
                self.opponents[opponent]['wins'] += 1
            else:
                self.opponents[opponent]['losses'] += 1

        self.game_count = self.wins + self.losses

    def analyze_matchups(self):
        """Analyze how this hero fared against all opponents.
            Summarize the deck's winrate as a whole and against each opponent hero encountered.
        """

        # All necessary calculations have already been done.
        # Print the matchup win rates.
        headers = ['opponent', 'games', 'wins', 'losses', 'win %']
        table = [['All', self.game_count, self.wins, self.losses, (self.wins / self.game_count) * 100]]

        # Sort opponents by frequency.
        for opponent, opponent_data in sorted(self.opponents.items(), key=lambda k_v: k_v[1]['games'], reverse=True):
            table.append([opponent, opponent_data['games'], opponent_data['wins'], opponent_data['losses'],
                          (opponent_data['wins'] / opponent_data['games']) * 100])

        print()
        print(tabulate(table, headers=headers, floatfmt='.2f'))

    def analyze_cards(self):
        """Analyze how the cards played by hero fared against all opponents.
            Summarize the card winrates as a whole.
            TODO: Make it easy to turn on/off the card vs. opponent winrates,
            maybe with a matchup threshold since this data can get very sparse.
        """

        # Card dictionary keyed by card name, value is a dict of win/loss data.
        cards = {}

        # Calculate the per card win rates against the various opponents.
        for game in self.games:
            opponent = game.opponent

            for card_name in game.cards():
                cards[card_name] = cards.get(card_name, {'games': 0, 'wins': 0, 'losses': 0, 'opponents': {}})
                cards[card_name]['games'] += 1
                if game.won():
                    cards[card_name]['wins'] += 1
                else:
                    cards[card_name]['losses'] += 1

                cards[card_name]['opponents'][opponent] = cards[card_name]['opponents'].get(opponent, {'games': 0, 'wins': 0, 'losses': 0})
                cards[card_name]['opponents'][opponent]['games'] += 1
                if game.won():
                    cards[card_name]['opponents'][opponent]['wins'] += 1
                else:
                    cards[card_name]['opponents'][opponent]['losses'] += 1

        # Calculate the various win percentages.
        for card, card_data in cards.items():
            card_data['win percentage'] = (card_data['wins'] / card_data['games']) * 100
            card_data['unplayed wins'] = self.wins - card_data['wins']
            card_data['unplayed losses'] = self.losses - card_data['losses']
            unplayed_games = card_data['unplayed wins'] + card_data['unplayed losses']
            card_data['unplayed percentage'] = 0 if unplayed_games == 0 else (card_data['unplayed wins'] / unplayed_games) * 100

            for opponent, opponent_data in card_data['opponents'].items():
                opponent_data['win percentage'] = (opponent_data['wins'] / opponent_data['games']) * 100
                opponent_data['unplayed wins'] = self.opponents[opponent]['wins'] - opponent_data['wins']
                opponent_data['unplayed losses'] = self.opponents[opponent]['losses'] - opponent_data['losses']
                unplayed_games = opponent_data['unplayed wins'] + opponent_data['unplayed losses']
                opponent_data['unplayed percentage'] = 0 if unplayed_games == 0 else (opponent_data['unplayed wins'] / (unplayed_games)) * 100
            
        card_headers = ['card vs. All', 'games', 'wins', 'losses', 'win %', 'unplayed wins', 'unplayed losses', 'unplayed %']
        card_table = []
        # Sort cards by best win percentage.
        cards_by_win_percent = []

        for card, card_data in sorted(cards.items(), key=lambda k_v: k_v[1]['win percentage'], reverse=True):
            cards_by_win_percent.append(card)
            card_table.append([card, card_data['games'], card_data['wins'], card_data['losses'], card_data['win percentage'],
                               card_data['unplayed wins'], card_data['unplayed losses'], card_data['unplayed percentage']])

        print()
        print(tabulate(card_table, headers=card_headers, floatfmt='.2f'))

        # Print the card vs. specific opponent analysis.
        # Note that this data really starts to suffer from sparse data.
        # TODO: make it easy to opt in/out of printing this.
        if False:
            for opponent in self.opponents.keys():
                card_headers = ['card vs. ' + opponent, 'games', 'wins', 'losses', 'win %', 'unplayed wins', 'unplayed losses', 'unplayed %']
                card_table = []
                for card in cards_by_win_percent:
                    # Not every card will have been played against every opponent.
                    if not opponent in cards[card]['opponents']:
                        continue
                    card_opponent_data = cards[card]['opponents'][opponent]
                    if card_opponent_data is None:
                        continue
                    card_table.append([card, card_opponent_data['games'], card_opponent_data['wins'], card_opponent_data['losses'],
                                       card_opponent_data['win percentage'], card_opponent_data['unplayed wins'],
                                       card_opponent_data['unplayed losses'], card_opponent_data['unplayed percentage']])
                
                print()
                print(tabulate(card_table, headers=card_headers, floatfmt='.2f'))

    def analyze_openings(self):
        """Analyze how the various turn 1, 2, 3 openings fared.
            Summarize the various opening win rates, ordered by the plays rather than win rates.
        """

        # Openings dictionary keyed by a turn 1-3 tuple of the cards played on those turn, value is a dict of win/loss data.
        openings = {}

        # Calculate the winrates of various openings.
        for game in self.games:
            opening = game.opening()
            openings[opening] = openings.get(opening, {'games': 0, 'wins': 0, 'losses': 0})
            openings[opening]['games'] += 1
            if game.won():
                openings[opening]['wins'] += 1
            else:
                openings[opening]['losses'] += 1

        for opening_data in openings.values():
            opening_data['win percentage'] = (opening_data['wins'] / opening_data['games']) * 100

        # Print the analysis of the openings.
        headers = ['turn 1', 'turn 2', 'turn 3', 'games', 'wins', 'losses', 'win %']
        table = []

        # Sort openings by the turn 1, 2, 3 plays.
        for opening, opening_data in sorted(openings.items(), key=lambda k_v: (sorted(k_v[0][0]), sorted(k_v[0][1]), sorted(k_v[0][2]))):
            table.append([sorted(opening[0]), sorted(opening[1]), sorted(opening[2]),
                          opening_data['games'], opening_data['wins'], opening_data['losses'], opening_data['win percentage']])

        print()
        print(tabulate(table, headers=headers, floatfmt='.2f'))

    def analyze_cards_by_turn(self, min_sample_size=5):
        """Analyze the win rates for the cards played on specific turns.
            This also suffers from sparse data so by default only shows data when a card is played
            on a turn 5 or more times.
        """

        # Turns dictionary keyed by the turn number e.g. 1, 2, 3.
        turns = {}

        # Calculate the win rates of cards played on specific turns.
        for game in self.games:
            last_turn = game.last_turn()
            if not last_turn:
                continue

            for turn in range(1, last_turn):
                cards = game.cards_on_turn(turn) or {'pass'}
                turns[turn] = turns.get(turn, {'cards': {}})

                for card in cards:
                    turns[turn]['cards'][card] = turns[turn]['cards'].get(card, {'games': 0, 'wins': 0, 'losses': 0})
                    turns[turn]['cards'][card]['games'] += 1
                    if game.won():
                        turns[turn]['cards'][card]['wins'] += 1
                    else:
                        turns[turn]['cards'][card]['losses'] += 1

        for turn, turn_data in turns.items():
            for card_data in turn_data['cards'].values():
                card_data['win percentage'] = (card_data['wins'] / card_data['games']) * 100

        # Print the analysis of the turns and cards played.
        headers = ['turn', 'play', 'games', 'wins', 'losses', 'win %']
        table = []

        # Sort by turn, then win rate.
        for turn, turn_data in turns.items():
            for card, card_data in sorted(turn_data['cards'].items(), key=lambda k_v: k_v[1]['win percentage'], reverse=True):
                # Ignore small samples.
                if card_data['games'] < min_sample_size:
                    continue
                table.append([turn, card, card_data['games'], card_data['wins'], card_data['losses'], card_data['win percentage']])

        print()
        print(tabulate(table, headers=headers, floatfmt='.2f'))

    def analyze_mana(self):
        """Analyze the win rates for mana differential between what the hero spent and what
            the opponent spent each game. A negative differential means the opponent spent more mana.
        """

        # mana differential dictionary keyed by differential buckets.
        mana_differentials = {}

        # Provide a description of the 5 differential buckets.
        keys = ['big disadvantage:          -8+',
                'slight disadvantage: -7 to -3',
                'about even:          -2 to  2',
                'slight advantage:     3 to  7',
                'big advantage:              8+']

        # Calculate the win rates for the mana differentials.
        for game in self.games:
            mana_differential = game.mana_differential()
            key = keys[4]
            if mana_differential < -7:
                key = keys[0]
            elif mana_differential < -2:
                key = keys[1]
            elif mana_differential < 2:
                key = keys[2]
            elif mana_differential < 8:
                key = keys[3]

            mana_differentials[key] = mana_differentials.get(key, {'games': 0, 'wins': 0, 'losses': 0})
            mana_differentials[key]['games'] += 1
            if game.won():
                mana_differentials[key]['wins'] += 1
            else:
                mana_differentials[key]['losses'] += 1

        # Print the analysis.
        headers = ['mana differential', 'games', 'wins', 'losses', 'win %']
        table = []

        # The differential bucket list is in display order.
        for key in keys:
            table.append([key, mana_differentials[key]['games'], mana_differentials[key]['wins'], mana_differentials[key]['losses'],
                          (mana_differentials[key]['wins'] / mana_differentials[key]['games']) * 100])

        print()
        print(tabulate(table, headers=headers, floatfmt='.2f'))
