import neat
import GameFactory
from Player.Player import Player
from Games.ConnectFour.V2.ConnectFourPlayerV2 import ConnectFourPlayerV2

game = GameFactory.Games.ConnectFour
version = 2
file_name = "12_1_2023_19"

arr = [0, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 2, 0, 0, 0,
       0, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 2, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0
       ]
print("TEST 1")
# One's Turn next
print(str(ConnectFourPlayerV2.in_a_row_count(1, arr, 0) == 1))
print(ConnectFourPlayerV2.in_a_row_count(2, arr, 1) == 1)

arr = [0, 1, 2, 1, 0, 0, 0,
       0, 0, 1, 2, 0, 0, 0,
       0, 0, 2, 1, 0, 0, 0,
       0, 0, 0, 2, 0, 0, 0,
       0, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0
       ]
# Two's turn next
print("TEST 2")
print(ConnectFourPlayerV2.in_a_row_count(1, arr, 0) == 1)
print(ConnectFourPlayerV2.in_a_row_count(2, arr, 1) == 1)

arr = [0, 1, 2, 1, 0, 0, 0,
       0, 0, 1, 2, 0, 0, 0,
       0, 0, 2, 1, 0, 0, 0,
       0, 0, 2, 2, 0, 0, 0,
       0, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0
       ]
# One's turn next
print("TEST 3")
print(ConnectFourPlayerV2.in_a_row_count(1, arr, 0) == 1)
print(ConnectFourPlayerV2.in_a_row_count(2, arr, 1) == 2)

arr = [0, 0, 1, 1, 0, 0, 0,
       0, 0, 2, 2, 0, 0, 0,
       0, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 2, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0
       ]
# One's turn next
print("Test 4")
print(ConnectFourPlayerV2.in_a_row_count(1, arr, 0) == 2 + 2/3.0)
print(ConnectFourPlayerV2.in_a_row_count(2, arr, 1) == 2 + 2/3.0)

exit()

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
