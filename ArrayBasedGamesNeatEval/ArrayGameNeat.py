from __future__ import annotations

from typing import Callable

import neat
from Player.Player import Player
from Enums.Games import Games
from GameInterfaces.IArrayGame import IArrayGame
from GameInterfaces.IPlayer import IPlayer
import GameFactory
from Evaluate import get_eval_func


def run(config_file,
        save_path,
        create_game: Callable[[list[IPlayer], int | None], IArrayGame],
        create_player: Callable[[any], IPlayer],
        save: bool):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    debug = {
        "debug": True,
        "win": False,
        "loss": False,
        "tie": True,
        "max": True,
        "invalid": True,
        "avg": True,
        "number of games check": False,
        "consistent games check": False,
        "show best game": True,
        "show best": True
    }
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    if save:
        p.add_reporter(neat.Checkpointer(
            5,
            filename_prefix=save_path)
        )

    # Run for up to 300 generations
    winner = p.run(
        get_eval_func(
            create_game,
            create_player,
            20,
            debug,
            0,
            .5
        ),
        100)
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.RecurrentNetwork.create(winner, config)
    game = create_game([
        create_player(winner_net),
        create_player(winner_net)
    ],
        0)
    game.play_game(True)
    print(game.invalid_move_loss)

    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    ai = create_player(winner_net)
    me = Player("Teddy")
    game = create_game([me, ai], 1)
    print(game.play_game(True))


def main():
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    config_path, save_path, create_game, create_player = (
        GameFactory.get_game(Games.ConnectFour, 4))

    run(config_path, save_path, create_game, create_player, False)


if __name__ == '__main__':
    main()
