import neat

from ArrayBasedGamesNeatEval.Enums.Games import Games

from ArrayBasedGamesNeatEval.Games.TicTacToe.TicTacToe import TicTacToe
from ArrayBasedGamesNeatEval.Games.TicTacToe.V1.TicTacToePlayer import TicTacToePlayer
from ArrayBasedGamesNeatEval.Games.TicTacToe.V2.TicTacToePlayerV2 import TicTacToePlayerV2
from ArrayBasedGamesNeatEval.Games.TicTacToe.V3.TicTacToePlayerV3 import TicTacToePlayerV3

from ArrayBasedGamesNeatEval.Games.ConnectFour.ConnectFour import ConnectFour
from ArrayBasedGamesNeatEval.Games.ConnectFour.V1.ConnectFourPlayerV1 import ConnectFourPlayerV1
from ArrayBasedGamesNeatEval.Games.ConnectFour.V2.ConnectFourPlayerV2 import ConnectFourPlayerV2
from ArrayBasedGamesNeatEval.Games.ConnectFour.V3.ConnectFourPlayerV3 import ConnectFourPlayerV3
from ArrayBasedGamesNeatEval.Games.ConnectFour.V4.ConnectFourPlayerV4 import ConnectFourPlayerV4


from ArrayBasedGamesNeatEval.Evaluate import dummy_eval

import os


# returns a population object from a specified file
def load_population(game: Games, version: int, file_name):
    path = get_save_path(game, version) + str(file_name)
    return neat.Checkpointer.restore_checkpoint(path)


# Loads the winner network from among the specified population file
def load_winner_net(game: Games, version: int, file_name):
    return load_population(game, version, file_name).run(dummy_eval, 1)


# returns the base path for accessing game files
def get_base_path(game: Games, version: int = -1):
    local_dir = os.path.dirname(__file__)
    base_path = ""
    if game == Games.TicTacToe:
        if version == -1:
            version_string = "V3"
        else:
            version_string = "V" + str(version)
        base_path = os.path.join(
            local_dir,
            'Games',
            'TicTacToe',
            version_string)
    elif game == Games.ConnectFour:
        if version == -1:
            version_string = "V4"
        else:
            version_string = "V" + str(version)
        base_path = os.path.join(
            local_dir,
            'Games',
            'ConnectFour',
            version_string)
    return base_path


# Creates the path for the configuration file for the requested game + version
def get_config_path(game: Games, version: int = -1):
    config_path = ""
    if game == Games.TicTacToe:
        config_path = os.path.join(
            get_base_path(game, version),
            'tic_tac_toe.txt')
    elif game == Games.ConnectFour:
        config_path = os.path.join(
            get_base_path(game, version),
            'connect_four.txt')
    return config_path


# gets the path for where to save winner files
def get_save_path(game: Games, version: int = -1):
    save_path = ""
    if game == Games.TicTacToe:
        save_path = os.path.join(
            get_base_path(game, version),
            'NeuralNets',
            'Net_'
        )
    elif game == Games.ConnectFour:
        save_path = os.path.join(
            get_base_path(game, version),
            'NeuralNets',
            'Net_'
        )
    return save_path


# Gets the function for creating the game
def get_game_func(game: Games):
    if game == Games.TicTacToe:
        return TicTacToe
    elif game == Games.ConnectFour:
        return ConnectFour


# gets the function for creating the player
def get_player_func(game: Games, version: int = -1):
    if game == Games.TicTacToe:
        if version == -1:
            return TicTacToePlayerV3
        else:
            if version == 1:
                return TicTacToePlayer
            if version == 2:
                return TicTacToePlayerV2
            if version == 3:
                return TicTacToePlayerV3

    elif game == Games.ConnectFour:
        if version == -1:
            return ConnectFourPlayerV4
        else:
            if version == 1:
                return ConnectFourPlayerV1
            if version == 2:
                return ConnectFourPlayerV2
            if version == 3:
                return ConnectFourPlayerV3
            if version == 4:
                return ConnectFourPlayerV4


# If the version is left unpopulated the latest version will be taken
def get_game(game: Games, version: int = -1):
    config_path = get_config_path(game, version)
    game_func = get_game_func(game)
    player_func = get_player_func(game, version)
    save_path = get_save_path(game, version)
    return config_path, save_path, game_func, player_func
