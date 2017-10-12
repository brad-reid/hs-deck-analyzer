# hs-deck-analyzer
Analyze Hearthstone decks using Track-o-bot data.

Provides reports aimed at helping players make deck building, mulligan and game play decisions.
The report format is also designed to make it easy to include your analysis results in reddit posts.

## Getting Started

You'll need to run the analyzer yourself for your game data.

### Prerequisites

#### Track-o-bot

You need to be using Track-o-bot. For details on installing and using Track-o-bot, visit:
https://trackobot.com/

#### Python

You'll need to install python on your system if you don't have it already.
For details on downloading and installing python, visit:
https://www.python.org/downloads/

#### Git

Using git will make it easy to check out and run a copy of the analyzer.
For details on downloading and installing git, visit:
https://git-scm.com/downloads

### Installing

TODO

## Additional Resources

TODO: Add links and descriptions for other available tools and websites that help analyze decks and game play.

## TODO/Wishlist
TODO: Add details about things I'd like to do. Unfortunately most of this stuff is larger than just this tool.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

# Example output

Here's an example report:

```
> py hs-deck-analyzer.py -u little-tundra-rhino-2171 -t <API_TOKEN> -c Rogue -s 5
```

## Rogue Matchup Win Rates
Opponents are ordered by frequency, making it easy to see performance against the most common matchups.
This data helps answer questions about how well your hero is performing against the meta you're facing
and how well you're performing against the opponents you are targeting.

| opponent   |   games |   wins |   losses |   win % |
|:-----------|--------:|-------:|---------:|--------:|
| All        |      50 |     28 |       22 |   56.00 |
| Rogue      |      15 |      8 |        7 |   53.33 |
| Priest     |      11 |      6 |        5 |   54.55 |
| Warlock    |       8 |      4 |        4 |   50.00 |
| Druid      |       7 |      4 |        3 |   57.14 |
| Shaman     |       4 |      3 |        1 |   75.00 |
| Hunter     |       2 |      1 |        1 |   50.00 |
| Mage       |       2 |      2 |        0 |  100.00 |
| Warrior    |       1 |      0 |        1 |    0.00 |

## Card Win Rates
Cards are ordered by win rate. Played % shows the percentage of games where you played the card.
Track-o-bot only has data for the cards played, so the unplayed columns are
attempting to help answer questions about how the deck performs when you don't draw that card or it sits in your hand.
Note that data is only shown when a card is played on a turn at least 5 times.

| card vs. All         |   wins |   win % |   games |   played % |   unplayed wins |   unplayed losses |   unplayed win % |
|:---------------------|-------:|--------:|--------:|-----------:|----------------:|------------------:|-----------------:|
| Leeroy Jenkins       |     11 |   91.67 |      12 |      24.00 |              17 |                21 |            44.74 |
| Shadowstep           |      9 |   69.23 |      13 |      26.00 |              19 |                18 |            51.35 |
| Southsea Deckhand    |     22 |   62.86 |      35 |      70.00 |               6 |                 9 |            40.00 |
| The Coin             |     14 |   60.87 |      23 |      46.00 |              14 |                13 |            51.85 |
| Naga Corsair         |      9 |   60.00 |      15 |      30.00 |              19 |                16 |            54.29 |
| SI:7 Agent           |     21 |   60.00 |      35 |      70.00 |               7 |                 8 |            46.67 |
| Southsea Captain     |     19 |   59.38 |      32 |      64.00 |               9 |                 9 |            50.00 |
| Cobalt Scalebane     |     13 |   59.09 |      22 |      44.00 |              15 |                13 |            53.57 |
| Edwin VanCleef       |      8 |   57.14 |      14 |      28.00 |              20 |                16 |            55.56 |
| Eviscerate           |     12 |   57.14 |      21 |      42.00 |              16 |                13 |            55.17 |
| Prince Valanar       |      4 |   57.14 |       7 |      14.00 |              24 |                19 |            55.81 |
| Patches the Pirate   |     28 |   56.00 |      50 |     100.00 |               0 |                 0 |             0.00 |
| Dagger Mastery       |     27 |   55.10 |      49 |      98.00 |               1 |                 0 |           100.00 |
| Shaku, the Collector |      6 |   54.55 |      11 |      22.00 |              22 |                17 |            56.41 |
| Bonemare             |      7 |   53.85 |      13 |      26.00 |              21 |                16 |            56.76 |
| Cold Blood           |     10 |   52.63 |      19 |      38.00 |              18 |                13 |            58.06 |
| Swashburglar         |     20 |   52.63 |      38 |      76.00 |               8 |                 4 |            66.67 |
| Fire Fly             |     19 |   50.00 |      38 |      76.00 |               9 |                 3 |            75.00 |
| Golakka Crawler      |     13 |   48.15 |      27 |      54.00 |              15 |                 8 |            65.22 |
| Vilespine Slayer     |     11 |   47.83 |      23 |      46.00 |              17 |                10 |            62.96 |
| Backstab             |     13 |   44.83 |      29 |      58.00 |              15 |                 6 |            71.43 |
| Flame Elemental      |     10 |   40.00 |      25 |      50.00 |              18 |                 7 |            72.00 |

## Opening Sequence Win Rates
Openings are your plays for the first 3 turns.
This data attempts to help answer questions about what cards you should mulligan for and which play sequences are strongest.
Unfortunately, this data is usually quite sparse.

Found 37 different openings in 50 games:

| turn 1                                      | turn 2                                                       | turn 3                                                                                   |   games |   wins |   losses |   win % |
|:--------------------------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------------------------------------|--------:|-------:|---------:|--------:|
| []                                          | ['Backstab', 'Dagger Mastery']                               | ['Dagger Mastery', 'Southsea Deckhand']                                                  |       1 |      1 |        0 |  100.00 |
| []                                          | ['Dagger Mastery']                                           | ['Backstab', 'SI:7 Agent']                                                               |       3 |      1 |        2 |   33.33 |
| []                                          | ['Dagger Mastery']                                           | ['Dagger Mastery']                                                                       |       1 |      0 |        1 |    0.00 |
| []                                          | ['Dagger Mastery']                                           | ['Patches the Pirate', 'SI:7 Agent', 'Swashburglar', 'The Coin']                         |       1 |      0 |        1 |    0.00 |
| []                                          | ['Dagger Mastery']                                           | ['Patches the Pirate', 'Southsea Captain', 'The Coin']                                   |       1 |      0 |        1 |    0.00 |
| []                                          | ['Dagger Mastery']                                           | ['Shaku, the Collector']                                                                 |       1 |      0 |        1 |    0.00 |
| []                                          | ['Dagger Mastery']                                           | ['Southsea Captain']                                                                     |       1 |      1 |        0 |  100.00 |
| []                                          | ['Golakka Crawler']                                          | ['Dagger Mastery']                                                                       |       1 |      1 |        0 |  100.00 |
| []                                          | ['Golakka Crawler']                                          | ['Eviscerate', 'Patches the Pirate', 'Southsea Deckhand']                                |       1 |      1 |        0 |  100.00 |
| []                                          | ['Golakka Crawler']                                          | ['Golakka Crawler', 'Patches the Pirate', 'Swashburglar']                                |       1 |      1 |        0 |  100.00 |
| []                                          | ['SI:7 Agent', 'The Coin']                                   | ['Eviscerate', 'Fire Fly']                                                               |       1 |      1 |        0 |  100.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Backstab', 'Patches the Pirate', 'Southsea Captain']                                   |       2 |      1 |        1 |   50.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Backstab', 'SI:7 Agent']                                                               |       1 |      1 |        0 |  100.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Cold Blood', 'Flame Elemental', 'Patches the Pirate', 'Southsea Deckhand']             |       1 |      1 |        0 |  100.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Cold Blood', 'Patches the Pirate', 'Southsea Deckhand', 'Swashburglar']                |       1 |      0 |        1 |    0.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Defias Ringleader', 'Swashburglar']                                                    |       1 |      0 |        1 |    0.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Edwin VanCleef', 'Patches the Pirate', 'Shadowstep', 'Swashburglar', 'The Coin']       |       1 |      1 |        0 |  100.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Golakka Crawler', 'Patches the Pirate', 'Shadowstep', 'Swashburglar']                  |       1 |      0 |        1 |    0.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Golakka Crawler', 'Patches the Pirate', 'Swashburglar']                                |       1 |      0 |        1 |    0.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Patches the Pirate', 'Southsea Captain']                                               |       4 |      1 |        3 |   25.00 |
| ['Fire Fly']                                | ['Dagger Mastery']                                           | ['Shaku, the Collector']                                                                 |       3 |      2 |        1 |   66.67 |
| ['Fire Fly']                                | ['Dagger Mastery', 'Fire Fly', 'Flame Elemental']            | ['Backstab', 'Dagger Mastery', 'Patches the Pirate', 'Southsea Captain', 'Swashburglar'] |       1 |      0 |        1 |    0.00 |
| ['Fire Fly']                                | ['Golakka Crawler']                                          | ['Patches the Pirate', 'Southsea Captain']                                               |       2 |      2 |        0 |  100.00 |
| ['Fire Fly']                                | ['Golakka Crawler']                                          | ['Shaku, the Collector']                                                                 |       1 |      0 |        1 |    0.00 |
| ['Fire Fly']                                | ['SI:7 Agent', 'The Coin']                                   | ['Dagger Mastery', 'Patches the Pirate', 'Southsea Deckhand']                            |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Southsea Deckhand'] | ['Golakka Crawler']                                          | ['Shaku, the Collector']                                                                 |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Dagger Mastery']                                           | ['Backstab', 'SI:7 Agent']                                                               |       1 |      0 |        1 |    0.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Dagger Mastery']                                           | ['Dagger Mastery', 'Fire Fly']                                                           |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Dagger Mastery']                                           | ['Golakka Crawler']                                                                      |       2 |      2 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Dagger Mastery']                                           | ['Shaku, the Collector']                                                                 |       1 |      0 |        1 |    0.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Dagger Mastery']                                           | ['Southsea Captain']                                                                     |       4 |      2 |        2 |   50.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Dagger Mastery']                                           | ['Southsea Captain', 'Southsea Deckhand', 'The Coin']                                    |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Edwin VanCleef', 'Shadowstep', 'Swashburglar', 'The Coin'] | ['Dagger Mastery']                                                                       |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Fire Fly', 'Sanguine Reveler']                             | ['Dagger Mastery', 'Southsea Deckhand']                                                  |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['SI:7 Agent', 'The Coin']                                   | ['Dagger Mastery', 'SI:7 Agent', 'Shadowstep']                                           |       1 |      1 |        0 |  100.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Shadow Word: Pain']                                        | ['Backstab', 'SI:7 Agent']                                                               |       1 |      0 |        1 |    0.00 |
| ['Patches the Pirate', 'Swashburglar']      | ['Southsea Captain', 'The Coin']                             | ['Dagger Mastery', 'Southsea Deckhand']                                                  |       1 |      1 |        0 |  100.00 |

## Win Rates When Playing Cards on Specific Turns
Note that data is only shown when a card is played on a turn at least 5 times.
This data attempts to help answer questions about what cards you should mulligan for and which plays are strongest.
Furthermore, it can help validate whether your playstyle and plan for the deck is working.

|   turn | play                 |   games |   wins |   losses |   win % |
|-------:|:---------------------|--------:|-------:|---------:|--------:|
|      1 | Patches the Pirate   |      16 |     11 |        5 |   68.75 |
|      1 | Swashburglar         |      15 |     10 |        5 |   66.67 |
|      1 | pass                 |      13 |      7 |        6 |   53.85 |
|      1 | Fire Fly             |      21 |     10 |       11 |   47.62 |
|      2 | The Coin             |       5 |      5 |        0 |  100.00 |
|      2 | Golakka Crawler      |       7 |      6 |        1 |   85.71 |
|      2 | Dagger Mastery       |      36 |     16 |       20 |   44.44 |
|      3 | Southsea Deckhand    |       8 |      7 |        1 |   87.50 |
|      3 | Dagger Mastery       |       9 |      7 |        2 |   77.78 |
|      3 | Golakka Crawler      |       5 |      3 |        2 |   60.00 |
|      3 | Southsea Captain     |      16 |      8 |        8 |   50.00 |
|      3 | Patches the Pirate   |      19 |      9 |       10 |   47.37 |
|      3 | Shaku, the Collector |       7 |      3 |        4 |   42.86 |
|      3 | Backstab             |       9 |      3 |        6 |   33.33 |
|      3 | SI:7 Agent           |       7 |      2 |        5 |   28.57 |
|      3 | Swashburglar         |       8 |      2 |        6 |   25.00 |
|      4 | Swashburglar         |       6 |      5 |        1 |   83.33 |
|      4 | Backstab             |       6 |      4 |        2 |   66.67 |
|      4 | Golakka Crawler      |       6 |      4 |        2 |   66.67 |
|      4 | Dagger Mastery       |      15 |      9 |        6 |   60.00 |
|      4 | SI:7 Agent           |      10 |      6 |        4 |   60.00 |
|      4 | Southsea Captain     |       5 |      3 |        2 |   60.00 |
|      4 | The Coin             |      11 |      6 |        5 |   54.55 |
|      4 | Vilespine Slayer     |       6 |      3 |        3 |   50.00 |
|      4 | Southsea Deckhand    |       9 |      4 |        5 |   44.44 |
|      4 | Cold Blood           |       5 |      2 |        3 |   40.00 |
|      4 | Patches the Pirate   |       5 |      1 |        4 |   20.00 |
|      5 | Patches the Pirate   |       7 |      6 |        1 |   85.71 |
|      5 | Southsea Captain     |       9 |      7 |        2 |   77.78 |
|      5 | Naga Corsair         |       5 |      3 |        2 |   60.00 |
|      5 | SI:7 Agent           |       5 |      3 |        2 |   60.00 |
|      5 | Dagger Mastery       |      10 |      6 |        4 |   60.00 |
|      5 | Cobalt Scalebane     |       9 |      5 |        4 |   55.56 |
|      5 | Flame Elemental      |       6 |      2 |        4 |   33.33 |
|      5 | Backstab             |       6 |      2 |        4 |   33.33 |
|      5 | Fire Fly             |       5 |      1 |        4 |   20.00 |
|      6 | Naga Corsair         |       5 |      3 |        2 |   60.00 |
|      6 | Vilespine Slayer     |       8 |      4 |        4 |   50.00 |
|      6 | Southsea Deckhand    |       8 |      4 |        4 |   50.00 |
|      6 | Flame Elemental      |       5 |      2 |        3 |   40.00 |
|      6 | Dagger Mastery       |      16 |      6 |       10 |   37.50 |
|      7 | Bonemare             |       6 |      4 |        2 |   66.67 |
|      7 | Dagger Mastery       |      11 |      7 |        4 |   63.64 |
|      7 | Golakka Crawler      |       5 |      2 |        3 |   40.00 |
|      8 | Vilespine Slayer     |       5 |      3 |        2 |   60.00 |
|      8 | Dagger Mastery       |      10 |      5 |        5 |   50.00 |
|      9 | Dagger Mastery       |       7 |      4 |        3 |   57.14 |

## Mana Differential Win Rates
This is the difference in mana spent between you and your opponent.
Game % shows the percentage of games where this mana differential occurred.
Note that the game winner will usually take the last turn, which probably helps pad the mana spent in their favor.

| mana differential              |   games |   games % |   wins |   losses |   win % |
|:-------------------------------|--------:|----------:|-------:|---------:|--------:|
| big disadvantage:          -8+ |      10 |     20.00 |      1 |        9 |   10.00 |
| slight disadvantage: -7 to -3  |      10 |     20.00 |      2 |        8 |   20.00 |
| about even:          -2 to  2  |      10 |     20.00 |      8 |        2 |   80.00 |
| slight advantage:     3 to  7  |      15 |     30.00 |     13 |        2 |   86.67 |
| big advantage:              8+ |       5 |     10.00 |      4 |        1 |   80.00 |
