from tabulate import tabulate

class Hero(object):
    """Analyze how a specific hero performs.
        Output is preformatted for reddit.
        For reddit formatting tips see: https://www.reddit.com/r/reddit.com/comments/6ewgt/reddit_markdown_primer_or_how_do_you_do_all_that/c03nik6/
    """

    def __init__(self, games: list, hero: str, min_sample_size=0):
        """Create a new hero given a list of games and a hero.
            Games only count if they are ranked and some cards were played.
            If a minimum sample size is added, the card related analyses will only show data if there
            are at least that many results in the sample.
        """
        self.games = []
        self.hero = hero
        self.min_sample_size = min_sample_size
        self.wins = 0
        self.losses = 0

        # Opponent dictionary keyed by opponent hero name, value is a dict of win/loss data.
        self.opponents = {}

        # Perform initial calculations that get used by multiple analyses.
        # Only look at games where cards were played.
        # TODO: Only look at ranked games. Unfortunately Track-o-bot bugs sometimes and doesn't record ranked games as ranked.
        # TODO: To filter standard vs. wild you have to look at the cards.
        for game in filter(lambda x: x.hero == hero and x.had_played_cards(), games):
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
        self.win_percentage = (self.wins / self.game_count) * 100

    def _valid(self):
        """Test whether or not it's valid to perform an analysis for this hero."""
        return bool(self.game_count)

    def analyze_matchups(self):
        """Analyze how this hero fared against all opponents.
            Summarize the deck's winrate as a whole and against each opponent hero encountered.
        """

        if not self._valid():
            print("Can't analyze " + self.hero)
            return

        # All necessary calculations have already been done.
        # Print the matchup win rates.
        headers = ['opponent', 'games', 'wins', 'losses', 'win %']
        table = [['All', self.game_count, self.wins, self.losses, self.win_percentage]]

        # Sort opponents by frequency.
        for opponent, opponent_data in sorted(self.opponents.items(), key=lambda k_v: k_v[1]['games'], reverse=True):
            table.append([opponent, opponent_data['games'], opponent_data['wins'], opponent_data['losses'],
                          (opponent_data['wins'] / opponent_data['games']) * 100])

        print()
        print('## ' + self.hero + ' Matchup Win Rates')
        print('Opponents are ordered by frequency, making it easy to see performance against the most common matchups.')
        print("This data helps answer questions about how well your hero is performing against the meta you're facing ")
        print("and how well you're performing against the opponents you are targeting.")
        print()
        print(tabulate(table, headers=headers, floatfmt='.2f', tablefmt='pipe'))

    def analyze_cards(self):
        """Analyze how the cards played by hero fared against all opponents.
            Summarize the card winrates as a whole. Some cards can suffer from sparse data,
            especially if you are playing a deck that can pull in random cards.
            The output uses the hero's min sample size.
            Also performs per opponent analyses for opponents that were at least 10% of your games.
        """

        if not self._valid():
            return

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
            
        card_headers = ['card vs. All', 'wins', 'win %', 'games', 'played %', 'unplayed wins', 'unplayed losses', 'unplayed win %']
        card_table = []
        # Sort cards by best win percentage.
        cards_by_win_percent = []
        deck_percentage_inserted = False

        for card, card_data in sorted(cards.items(), key=lambda k_v: k_v[1]['win percentage'], reverse=True):
            # Ignore small samples.
            if card_data['games'] < self.min_sample_size:
                continue

            # Add a marker row for the deck win rate.
            if card_data['win percentage'] < self.win_percentage and not deck_percentage_inserted:
                deck_percentage_inserted = True
                card_table.append(['-- deck --', self.wins, self.win_percentage, self.game_count])

            cards_by_win_percent.append(card)
            card_table.append([card, card_data['wins'], card_data['win percentage'],
                               card_data['games'], (card_data['games'] / self.game_count) * 100,
                               card_data['unplayed wins'], card_data['unplayed losses'], card_data['unplayed percentage']])

        print()
        print('## Card Win Rates')
        print("Cards are ordered by win rate. Played % shows the percentage of games where you played the card.")
        print("Track-o-bot only has data for the cards played, so the unplayed columns are ")
        print("attempting to help answer questions about how the deck performs when you don't draw that card or it sits in your hand.")
        print("Note that data is only shown when a card is played on a turn at least " + repr(self.min_sample_size) + " times.")
        print()
        print(tabulate(card_table, headers=card_headers, floatfmt='.2f', tablefmt='pipe'))

        # Print the card vs. specific opponent analysis.
        # Note that this data really starts to suffer from sparse data.
        # For now, just show data for opponents that showed up in more than 10% of the games.
        for opponent in self.opponents.keys():
            opponent_game_count = self.opponents[opponent]['games']
            if opponent_game_count < self.game_count * .1:
                continue

            card_headers = [repr(opponent_game_count) + ' games vs. ' + opponent,
                            'wins', 'win %', 'games', 'played %', 'unplayed wins', 'unplayed losses', 'unplayed win %']
            card_table = []
            for card in cards_by_win_percent:
                # Not every card will have been played against every opponent.
                if not opponent in cards[card]['opponents']:
                    continue
                card_opponent_data = cards[card]['opponents'][opponent]
                if card_opponent_data is None:
                    continue
                card_table.append([card, card_opponent_data['wins'], card_opponent_data['win percentage'],
                                   card_opponent_data['games'], (card_opponent_data['games'] / opponent_game_count) * 100,
                                   card_opponent_data['unplayed wins'], card_opponent_data['unplayed losses'],
                                   card_opponent_data['unplayed percentage']])

            print()
            print(tabulate(card_table, headers=card_headers, floatfmt='.2f', tablefmt='pipe'))

        # Print a win rate summary of all cards against all opponents.
        # Generate the headers, ordered by opponent frequency.
        headers = ['Card', 'All (' + repr(self.game_count) + ')']
        opponents_by_frequency = []
        for opponent, opponent_data in sorted(self.opponents.items(), key=lambda k_v: k_v[1]['games'], reverse=True):
            opponents_by_frequency.append(opponent)
            headers.append(opponent + ' (' + repr(self.opponents[opponent]['games']) + ')')

        table = []
        deck_percentage_inserted = False

        for card in cards_by_win_percent:
            # Add a marker row for the deck win rate.
            if cards[card]['win percentage'] < self.win_percentage and not deck_percentage_inserted:
                deck_percentage_inserted = True
                deck_row = ['-- deck --', self.win_percentage]
                for opponent in opponents_by_frequency:
                    # Not every card will have been played against every opponent.
                    if not opponent in self.opponents:
                        deck_row.append(None)
                    else:
                        deck_row.append((self.opponents[opponent]['wins'] / self.opponents[opponent]['games']) * 100)
                table.append(deck_row)

            card_row = [card, cards[card]['win percentage']]

            for opponent in opponents_by_frequency:
                # Not every card will have been played against every opponent.
                if not opponent in cards[card]['opponents']:
                    card_row.append(None)
                else:
                    card_row.append(cards[card]['opponents'][opponent]['win percentage'])
            table.append(card_row)

        print()
        print('## Card Win Rate Summary')
        print('Summarize the win rates of the cards against all opponents.')
        print("Cards are ordered by their overall win rate, opponents are ordered by frequency and show the game count in parentheses.")
        print()
        print(tabulate(table, headers=headers, floatfmt='.2f', tablefmt='pipe'))

    def analyze_openings(self):
        """Analyze how the various turn 1, 2, 3 openings fared.
            Summarize the various opening win rates, ordered by the plays rather than win rates.
        """

        if not self._valid():
            return

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
        print('## Opening Sequence Win Rates')
        print("Openings are your plays for the first 3 turns.")
        print("This data attempts to help answer questions about what cards you should mulligan for and which play sequences are strongest.")
        print("Unfortunately, this data is usually quite sparse.")
        print()
        print('Found ' + repr(len(openings)) + ' different openings in ' + repr(self.game_count) + ' games:')
        print()
        print(tabulate(table, headers=headers, floatfmt='.2f', tablefmt='pipe'))

    def analyze_cards_by_turn(self):
        """Analyze the win rates for the cards played on specific turns.
            This also suffers from sparse data and uses the hero's min sample size.
        """

        if not self._valid():
            return

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
                if card_data['games'] < self.min_sample_size:
                    continue
                table.append([turn, card, card_data['games'], card_data['wins'], card_data['losses'], card_data['win percentage']])

        print()
        print('## Win Rates When Playing Cards on Specific Turns')
        print("Note that data is only shown when a card is played on a turn at least " + repr(self.min_sample_size) + " times.")
        print("This data attempts to help answer questions about what cards you should mulligan for and which plays are strongest.")
        print("Furthermore, it can help validate whether your playstyle and plan for the deck is working.")
        print()
        print(tabulate(table, headers=headers, floatfmt='.2f', tablefmt='pipe'))

    def analyze_mana(self):
        """Analyze the win rates for mana differential between what the hero spent and what
            the opponent spent each game. A negative differential means the opponent spent more mana.
        """

        if not self._valid():
            return

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
        headers = ['mana differential', 'games', 'games %', 'wins', 'losses', 'win %']
        table = []

        # The differential bucket list is in display order.
        for key in keys:
            if key not in mana_differentials:
                continue

            table.append([key, mana_differentials[key]['games'], (mana_differentials[key]['games'] / self.game_count) * 100,
                          mana_differentials[key]['wins'], mana_differentials[key]['losses'],
                          (mana_differentials[key]['wins'] / mana_differentials[key]['games']) * 100])

        print()
        print('## Mana Differential Win Rates')
        print("This is the difference in mana spent between you and your opponent.")
        print("Game % shows the percentage of games where this mana differential occurred.")
        print("Note that the game winner will usually take the last turn, which probably helps pad the mana spent in their favor.")
        print()
        print(tabulate(table, headers=headers, floatfmt='.2f', tablefmt="pipe"))

    def analyze_games_by_rank(self):
        """Analyze the win rates for the deck at the different levels of ranked ladder play.
            TODO: Validate how legend games show up.
            TODO: Make it possible to ignore games above certain ranks.
        """

        if not self._valid():
            return

        # Ranks dictionary keyed by ladder rank.
        ranks = {}

        # Calculate the win rates for the various ranks.
        for game in self.games:
            rank = game.rank

            ranks[rank] = ranks.get(rank, {'games': 0, 'wins': 0, 'losses': 0})
            ranks[rank]['games'] += 1
            if game.won():
                ranks[rank]['wins'] += 1
            else:
                ranks[rank]['losses'] += 1

        # Print the analysis.
        headers = ['ladder rank', 'games', 'wins', 'losses', 'win %']
        table = []

        # Sort by rank in ladder order, high ranks first.
        for rank, rank_data in sorted(ranks.items(), reverse=True):
            table.append([rank, rank_data['games'], rank_data['wins'], rank_data['losses'],
                          (rank_data['wins'] / rank_data['games']) * 100])

        print()
        print('## Ladder Rank Win Rates')
        print("This shows how the hero performed at the different ladder ranks.")
        print("This should help you gauge whether or not games at easier ranks are affecting the stats.")
        print()
        print(tabulate(table, headers=headers, floatfmt='.2f', tablefmt="pipe"))
