import requests
import argparse
import datetime
import json

from game import Game
from hero import Hero

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', type=str,
                    help='Your track-o-bot username')
parser.add_argument('-t', '--token', type=str,
                    help='Your track-o-bot API token')
parser.add_argument('-i', '--infile', type=str,
                    help='The name of a file containing json data for the games you want to analyze.'
                    + 'If a file is specified, it will be used instead of fetching data.')
parser.add_argument('-o', '--outfile', type=str, default='trackobot_games.json',
                    help='The name of a file to store the json data for the games fetched from track-o-bot. '
                    + 'When run in fetch mode, always writes the data fetched.')
parser.add_argument('-c', '--hero', type=str,
                    help='The hero class you want to analyze, e.g. Mage. If not specified all games will be analyzed with a simple summary.')
args = parser.parse_args()

if not args.infile and not (args.username and args.token):
    parser.print_help()
    parser.error('You must specify either your username and token or an input file.')

# Get the game data to analyze.
games = []

if args.infile:
    with open(args.infile) as game_data:    
        for g in json.load(game_data):
            games.append(Game(g))
            print(games[-1])
else:
    print('Fetching game data from Track-o-bot for ' + args.username)
    trackobot_url = 'https://trackobot.com/profile/history.json'
    parameters = {'username': args.username, 'token': args.token, 'page': 0}

    # Get all the pertinent track-o-bot games.
    # Track-o-bot only has per card data from the last 10 days.
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    found_last_game = False
    games_json = []

    while not found_last_game:
        parameters['page'] += 1
        r = requests.get(trackobot_url, params=parameters)
        r.raise_for_status()

        for g in r.json()['history']:
            game = Game(g)
            print(game)
            if game.date < ten_days_ago.isoformat():
                print('Done getting games from the last 10 days.')
                found_last_game = True
                break
            else:
                games.append(game)
                games_json.append(g)

    # Always save the trackobot data, making it easy to re-run without having to re-fetch.
    with open('trackobot_games.json', 'w') as fp:
        json.dump(games_json, fp)

# Ready to start analyzing the games.
total_games = len(games)
print('Analyzing ' + repr(total_games) + ' games.')

# Give a quick W/L summary of the games
wins = 0
losses = 0

for game in games:
    if (not args.hero) or (args.hero == game.hero):
        if game.won():
            wins += 1
        else:
            losses += 1

if args.hero:
    print(args.hero + ' games')
else:
    print('All games')

print(repr(wins) + ' wins')
print(repr(losses) + ' losses')
print('{:.2%} win percentage'.format(wins/(wins + losses)))

# Perform a more detailed analysis for the specified hero class.
# TODO: Make it easy to turn on/off the various analyses. What's the right way to do that with argparse?
if args.hero:
   hero = Hero(games, args.hero)
   hero.analyze_matchups()
   hero.analyze_cards()
   hero.analyze_openings()
   hero.analyze_cards_by_turn()



