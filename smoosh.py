import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infiles', type=str, nargs="*", default=[],
                    help='The names of files containing json data for the games you want to analyze. '
                    + 'Puts all the games in one list, de-duping them based on game id.')
parser.add_argument('-o', '--outfile', type=str, default='smooshed_games.json',
                    help='The name of a file to store the json data for the games.')
parser.add_argument('-c', '--hero', type=str,
                    help='The hero class you want to analyze, e.g. Mage. If not specified all games will be analyzed with a simple summary.')
parser.add_argument('-k', '--deck', type=str,
                    help='The deck name you want to analyze, e.g. Other. If not specified all decks will be analyzed with a simple summary.')

args = parser.parse_args()

# Get the game data to analyze.
games = []
seen = set()

for infile in args.infiles:
    with open(infile) as game_data:    
        for g in json.load(game_data):
            print(g)
            if (g['id'] not in seen) and (not args.hero or args.hero == g['hero']) and (not args.deck or args.deck == g['deck']):
                games.append(g)
                seen.add(g['id'])
                print('added game ' + repr(g['id']))

with open(args.outfile, 'w') as fp:
    json.dump(games, fp)

print('Wrote ' + repr(len(games)) + ' games to ' + args.outfile)
