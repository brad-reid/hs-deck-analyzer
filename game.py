class Game(object):
    """A class to encapsulate game data returned from track-o-bot.

    Attributes:
        game_data: A dictionary representing a single game
    """

    def __init__(self, game_data: dict):
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
    
    def cards(self):
        """Return the set of cards that the hero (not the opponent) played this game."""
        return set(map(lambda y : y['card']['name'], filter(lambda x : x['player'] == 'me', self.game_data['card_history'])))

    def cards_on_turn(self, turn: int):
        """Return a frozenset of cards that the hero played on the specified turn. The first turn is 1."""
        return frozenset(map(lambda y : y['card']['name'],
                             filter(lambda x : x['player'] == 'me' and x['turn'] == turn, self.game_data['card_history'])))

    def opening(self):
        """Return a tuple of frozensets of the cards played each turn on the first 3 turns of this game.
            e.g. (frozenset({'Mana Wyrm'}), frozenset({'Arcanologist'}), frozenset({'Mirror Entity', 'Kirin Tor Mage'}))
        """
        return (self.cards_on_turn(1), self.cards_on_turn(2), self.cards_on_turn(3))
