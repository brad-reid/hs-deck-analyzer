class Game(object):
    """A class to encapsulate game data returned from track-o-bot."""

    def __init__(self, game_data: dict):
        """Create a new game given a track-o-bot dictionary representing a single game."""
        self.game_data = game_data

    @property
    def hero(self):
        return self.game_data['hero']

    # If track-o-bot hasn't identified a deck, it will be left null.
    # The track-o-bot website shows these games as "Other"
    @property
    def deck(self):
        return self.game_data['hero_deck'] or 'Other'

    @property
    def opponent(self):
        return self.game_data['opponent']

    @property
    def opponent_deck(self):
        return self.game_data['opponent_deck'] or 'Other'

    @property
    def date(self):
        return self.game_data['added']

    # Simplify the result to W/L
    # What about draws?
    @property
    def result(self):
        return 'W' if self.game_data['result'] == 'win' else 'L'

    def __str__(self):
        return self.result + ': ' + self.deck + ' ' + self.hero + ' vs. ' + self.opponent_deck + ' ' + self.opponent + ' on ' + self.date
        
    def won(self):
        return self.game_data['result'] == 'win'

    def card_history(self, player='me'):
        """Return an iterator for all the cards played by the specified player.
            Defaults to the hero, 'me', specify 'opponent' for the opponent's cards.
        """
        return filter(lambda x : x['player'] == player, self.game_data['card_history'])
    
    def cards(self):
        """Return the set of card names that the hero (not the opponent) played this game."""
        return set(map(lambda y : y['card']['name'], self.card_history()))

    def cards_on_turn(self, turn: int):
        """Return a frozenset of cards that the hero played on the specified turn. The first turn is 1."""
        return frozenset(map(lambda y : y['card']['name'],
                             filter(lambda x : x['player'] == 'me' and x['turn'] == turn, self.game_data['card_history'])))

    def opening(self):
        """Return a tuple of frozensets of the cards played each turn on the first 3 turns of this game.
            e.g. (frozenset({'Mana Wyrm'}), frozenset({'Arcanologist'}), frozenset({'Mirror Entity', 'Kirin Tor Mage'}))
        """
        return (self.cards_on_turn(1), self.cards_on_turn(2), self.cards_on_turn(3))

    def last_turn(self):
        """Find the last turn taken by the hero in this game."""
        return max(map(lambda x: x['turn'], self.card_history()), default=0)

    def mana_spent(self, player='me'):
        """Get the total mana spent by the specified player across all the turns in the game.
            Defaults to the hero, 'me', specify 'opponent' for the opponent's mana spent.
        """
        return sum(map(lambda x: x['card']['mana'], self.card_history(player)))

    def mana_differential(self):
        """Get the differential between the mana spent by the hero and the opponent over the course of the game.
            A negative number means the opponent spent more mana.
        """
        return self.mana_spent() - self.mana_spent('opponent')
