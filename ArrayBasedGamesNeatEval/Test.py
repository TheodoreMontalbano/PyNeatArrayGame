import neat
from ArrayBasedGamesNeatEval import GameFactory
from ArrayBasedGamesNeatEval.Player.Player import Player

game = GameFactory.Games.ConnectFour
version = 2
file_name = "12_1_2023_19"

config_path, _, create_game, _ = (
    GameFactory.get_game(game, version))

create_player = GameFactory.get_player_func(game, 3)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.RecurrentNetwork.create(
    GameFactory.load_winner_net(
        game,
        version,
        file_name),
    config
)

print(create_game([
        create_player(net),
        create_player(net)
    ],
        0
).play_game(True))
