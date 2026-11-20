# Echecs-L1ST

A chess game in Python with a Pygame interface. Play against a bot or against a friend over the network.
The game rules, the interface, the network code and the AI are all written from scratch (the interface is in French).

## Features

- **Solo mode** against a bot, with two difficulty levels (Easy: search depth 2, Medium: depth 4)
- **Online multiplayer** over TCP sockets: one player hosts, the other joins with an IP and a port
- **Rules engine**: every piece type, starting position loaded from a FEN string, win and draw detection (threefold repetition, insufficient material, no-progress limit)
- **Bot-vs-bot runner** (`tournoi.py`) to compare engines

## The bot

`bots/negamax.py` is a Negamax search with:

- alpha-beta pruning
- a **transposition table** keyed by a **Zobrist hash** of the board
- **iterative deepening** under a time limit
- **move ordering**: captures first, best material gain first
- an evaluation made of material plus **piece-square tables**

## Run it

Tested with Python 3.11.

```sh
pip install pygame pygame-widgets
python main.py
```

For online games, the default port and address are in `config.json`.

To let the bot play against a random player:

```sh
python tournoi.py
```

## Project layout

| Folder | Content |
| --- | --- |
| `moteur/` | Game rules: board, pieces, game state |
| `bots/` | Random bot and Negamax bot |
| `interface/` | Pygame menus and game screen |
| `multijoueur/` | Server and client |
| `assets/` | Images and sounds |

Started as a university project.
