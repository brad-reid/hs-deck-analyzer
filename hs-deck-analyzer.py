import argparse
import json

from game import Game
from hero import Hero
from trackobot import Trackobot

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', type=str,
                    help='Your track-o-bot username')
parser.add_argument('-t', '--token', type=str,
                    help='Your track-o-bot API token')
parser.add_argument('-i', '--infile', type=str,
                    help='The name of a file containing json data for the games you want to analyze. '
                    + 'If a file is specified, it will be used instead of fetching data.')
parser.add_argument('-o', '--outfile', type=str, default='trackobot_games.json',
                    help='The name of a file to store the json data for the games fetched from track-o-bot. '
                    + 'When run in fetch mode, always writes the data fetched.')
parser.add_argument('-c', '--hero', type=str,
                    help='The hero class you want to analyze, e.g. Mage. If not specified all games will be analyzed with a simple summary.')
parser.add_argument('-s', '--sample-size', type=int, default=0,
                    help='The minimum sample size to require when displaying results for card related analyses. ' +
                    'If not specified all data will be shown.')
parser.add_argument('-d', '--days', type=int, default=10,
                    help='The maximum number of days worth of data to fetch. Will not fetch more than 10 days.')
args = parser.parse_args()

# Get the game data to analyze.
games = []

if args.infile:
    with open(args.infile) as game_data:    
        for g in json.load(game_data):
            games.append(Game(g))
            print(games[-1])
elif args.username and args.token:
    print('Fetching game data from Track-o-bot for ' + args.username)
    trackobot = Trackobot(args.username, args.token, args.days)
    games = trackobot.get_game_history(args.outfile)
else:
    parser.print_help()
    parser.error('You must specify either your username and token or an input file.')


# Give a quick W/L summary for all the games
total_games = len(games)
wins = sum(1 for _ in filter(lambda x: x.won(), games))
losses = total_games - wins

print()
print('Analyzing ' + repr(total_games) + ' games.')
print(repr(wins) + ' wins')
print(repr(losses) + ' losses')
print('{:.2%} win percentage'.format(wins/(wins + losses)))

# Perform a more detailed analysis for the specified hero class.
# TODO: Make it easy to turn on/off the various analyses. What's the right way to do that with argparse?
if args.hero:
    print()
    print('--- Analyzing ' + args.hero + ' games ---')
    hero = Hero(games, args.hero, args.sample_size)
    hero.analyze_matchups()
    hero.analyze_cards()
    hero.analyze_openings()
    hero.analyze_cards_by_turn()
    hero.analyze_mana()
    hero.analyze_games_by_rank()



