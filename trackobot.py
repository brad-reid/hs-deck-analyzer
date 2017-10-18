import requests
import datetime
import json

from game import Game

class Trackobot(object):
    """A facade class for interacting with track-o-bot.
        Note: There is an existing python library for interacting with track-o-bot,
        https://github.com/ThaWeatherman/trackopy

        I've opted not to use that library since it requires your track-o-bot password,
        which is annoying for the average user to find and use. I prefer to use the
        easier to find API token, especially since we only want to read data.

    """

    def __init__(self, user: str, token: str, days=10):
        """Create a new track-o-bot interface for the given user, API token and number of days.
            Track-o-bot only stores card history for 10 days, so only retrieves a max of 10 days of data.
        """
        self.user = user
        self.token = token
        self.days = days if days <= 10 else 10

    def get_game_history(self, outfile: str):
        """Get the last 10 days of game data from Track-o-bot.
            Saves the json version of the game data to the specified output file.
            Returns a list of game dictionaries.
        """
        history_url = 'https://trackobot.com/profile/history.json'
        parameters = {'username': self.user, 'token': self.token, 'page': 0}

        # Get all the pertinent track-o-bot games.
        # Track-o-bot only has per card data from the last 10 days.
        ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=self.days)
        found_last_game = False
        games_json = []
        games = []

        while not found_last_game:
            # First page is 1.
            parameters['page'] += 1
            r = requests.get(history_url, params=parameters)
            r.raise_for_status()

            for g in r.json()['history']:
                game = Game(g)
                print(game)
                if game.date < ten_days_ago.isoformat():
                    print('Done getting games from the last ' + repr(self.days) + ' days.')
                    found_last_game = True
                    break
                else:
                    games.append(game)
                    games_json.append(g)

        # Always save the trackobot data, making it easy to re-run without having to re-fetch.
        with open(outfile, 'w') as fp:
            json.dump(games_json, fp)

        return games

