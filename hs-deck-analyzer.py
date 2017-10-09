import requests
import argparse
import datetime
import json

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
args = parser.parse_args()

if not args.infile and not (args.username and args.token):
    parser.print_help()
    parser.error('You must specify either your username and token or an input file.')

# Get the game data to analyze.
games = []

if args.infile:
    with open(args.infile) as game_data:    
        games = json.load(game_data)
else:
    print('Fetching game data from Track-o-bot for ' + args.username)
    trackobot_url = 'https://trackobot.com/profile/history.json'
    parameters = {'username': args.username, 'token': args.token, 'page': 0}

    # Get all the pertinent track-o-bot games.
    # Track-o-bot only has per card data from the last 10 days.
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    found_last_game = False

    while not found_last_game:
        parameters['page'] += 1
        r = requests.get(trackobot_url, params=parameters)
        r.raise_for_status()

        for game in r.json()['history']:
            print(game['result'] + ': ' + repr(game['hero_deck']) + ' ' + game['hero'] + ' vs. ' +
                  repr(game['opponent_deck']) + ' ' + game['opponent'] + ' ' + game['added'])
            if game['added'] < ten_days_ago.isoformat():
                print('Done getting games from the last 10 days.')
                found_last_game = True
                break
            else:
                games.append(game)

    print('Found ' + repr(len(games)) + ' games from the last 10 days.')    

    # Always save the trackobot data, making it easy to re-run without having to re-fetch.
    with open('trackobot_games.json', 'w') as fp:
        json.dump(games, fp)

# Ready to start analyzing the games.
print('Analyzing ' + repr(len(games)) + ' games.')
