from __future__ import annotations

import neat
from random import sample
from collections import deque
from typing import Callable

from GameInterfaces.IArrayGame import IArrayGame, IPlayer


def compare_players(create_array_game: Callable[[list[IPlayer], int | None], IArrayGame],
                    to_evaluate: IPlayer,
                    to_evaluate_id: int,
                    curr_tester: IPlayer,
                    curr_tester_id: int,
                    debug: dict[str, bool],
                    win_count: float,
                    max_move_num: int,
                    avg_move_num: float,
                    percent_tie: float,
                    percent_win: float,
                    percent_loss: float,
                    percent_invalid_move_loss: float,
                    win_track_dict: dict[tuple[int, int], int],
                    play_track_dict: dict[tuple[int, int], int]
                    ):
    same_pairing_different_result = False
    for j in range(2):
        curr_game = create_array_game(
            [
                to_evaluate,
                curr_tester
            ],
            j
        )
        result = curr_game.play_game()

        if "debug" in debug and debug["debug"]:
            if "max" in debug and debug["max"]:
                max_move_num = max(max_move_num, curr_game.move_num)
            if "avg" in debug and debug["avg"]:
                avg_move_num = avg_move_num + curr_game.move_num
            if result == 0:
                if "tie" in debug and debug["tie"]:
                    percent_tie = percent_tie + 1.0
            elif result == 1:
                if "won" in debug and debug["won"]:
                    percent_win = percent_win + 1.0
            else:
                if "loss" in debug and debug["loss"]:
                    percent_loss = percent_loss + 1.0
            if curr_game.invalid_move_loss:
                if "invalid" in debug and debug["invalid"]:
                    percent_invalid_move_loss = (
                            percent_invalid_move_loss + 1.0)

            # Check the last time the two players played the result was consistent
            if not (curr_tester_id == to_evaluate_id):
                if j == 0:
                    # Check wins are the same
                    if "consistent games check" in debug and debug["consistent games check"]:
                        if (to_evaluate_id, curr_tester_id) in win_track_dict:
                            if result == 0:
                                if not win_track_dict[(to_evaluate_id, curr_tester_id)] == result:
                                    same_pairing_different_result = True
                            else:
                                if win_track_dict[(to_evaluate_id, curr_tester_id)] == result:
                                    same_pairing_different_result = True
                        else:
                            win_track_dict[(to_evaluate_id, curr_tester_id)] = result
                    # Check each genome plays exactly twice
                    if "number of games check" in debug and debug["number of games check"]:
                        if (to_evaluate_id, curr_tester_id) in play_track_dict:
                            play_track_dict[(to_evaluate_id, curr_tester_id)] = \
                                play_track_dict[(to_evaluate_id, curr_tester_id)] + 1
                        else:
                            play_track_dict[(to_evaluate_id, curr_tester_id)] = 1
                else:
                    # Check wins are the same
                    if "consistent games check" in debug and debug["consistent games check"]:
                        if (curr_tester_id, to_evaluate_id) in win_track_dict:
                            if result == 0:
                                if not win_track_dict[(curr_tester_id, to_evaluate_id)] == result:
                                    same_pairing_different_result = True
                            else:
                                if win_track_dict[(curr_tester_id, to_evaluate_id)] == result:
                                    same_pairing_different_result = True
                        else:
                            win_track_dict[(curr_tester_id, to_evaluate_id)] = result
                    # Check each genome plays exactly twice
                    if "number of games check" in debug and debug["number of games check"]:
                        if (curr_tester_id, to_evaluate_id) in play_track_dict:
                            play_track_dict[(curr_tester_id, to_evaluate_id)] = \
                                play_track_dict[(curr_tester_id, to_evaluate_id)] + 1
                        else:
                            play_track_dict[(curr_tester_id, to_evaluate_id)] = 1

        if result == 0:
            win_count = win_count + 0.5
        elif result == 1:
            if curr_game.invalid_move_loss:
                win_count = (win_count + curr_game.move_num
                             / (curr_game.move_num + 1))
            else:
                win_count = win_count + 1.0
        else:
            win_count = (win_count - int(curr_game.invalid_move_loss)
                         / curr_game.move_num)
    return (win_count, max_move_num, avg_move_num, percent_tie,
            percent_win, percent_loss, percent_invalid_move_loss,
            same_pairing_different_result)


def get_eval_func(create_array_game: Callable[[list[IPlayer], int | None], IArrayGame],
                  create_player: Callable[[any], IPlayer],
                  sample_size: int,
                  debug: dict[str, bool],
                  winner_queue_length: int = 100,
                  winner_queue_weight: float = 0.5):
    winners_queue = deque()
    winners_queue_dict = {}

    def eval_genome(genomes, config):
        #### Debug Vars ####
        avg_move_num = 0
        max_move_num = 0
        test_num = 0
        percent_invalid_move_loss = 0.0
        percent_tie = 0.0
        percent_win = 0.0
        percent_loss = 0.0
        # The following vars will be used to track whether games are having consistent results with the same players
        same_pairing_different_result = False
        win_track_dict = {}
        play_track_dict = {}
        #####################
        max_genome = any
        max_id = 0
        max_fitness = float("-inf")
        for genome_id, genome in genomes:
            win_count = 0.0
            winners_queue_win_count = 0.0
            net = neat.nn.RecurrentNetwork.create(genome, config)
            to_evaluate = create_player(net)

            if len(genomes) <= sample_size:
                sample_set = genomes
                test_num = len(genomes)
            else:
                sample_set = sample(genomes, sample_size)
                test_num = sample_size

            for i in sample_set:
                curr_tester = create_player(neat.nn.RecurrentNetwork.create(i[1], config))

                (win_count, max_move_num, avg_move_num, percent_tie,
                 percent_win, percent_loss, percent_invalid_move_loss,
                 same_pairing_different_result) \
                    = compare_players(create_array_game,
                                      to_evaluate,
                                      genome_id,
                                      curr_tester,
                                      i[0],
                                      debug,
                                      win_count,
                                      max_move_num,
                                      avg_move_num,
                                      percent_tie,
                                      percent_win,
                                      percent_loss,
                                      percent_invalid_move_loss,
                                      win_track_dict,
                                      play_track_dict
                                      )
            for i in winners_queue:
                curr_tester = create_player(neat.nn.RecurrentNetwork.create(i[1], config))

                (winners_queue_win_count, _, _, _,
                 _, _, _, _) \
                    = compare_players(create_array_game,
                                      to_evaluate,
                                      genome_id,
                                      curr_tester,
                                      i[0],
                                      debug,
                                      winners_queue_win_count,
                                      0,
                                      0,
                                      0,
                                      0,
                                      0,
                                      0,
                                      {},
                                      {}
                                      )
            if len(winners_queue) > 0:
                genome.fitness = (win_count / (2.0 * test_num) * (1 - winner_queue_weight)
                                  + winner_queue_weight * winners_queue_win_count / len(winners_queue * 2))
            else:
                genome.fitness = win_count / (2.0 * test_num)

            if genome.fitness > max_fitness:
                max_fitness = genome.fitness
                max_genome = genome
                max_id = genome_id
        # Update the winners queue
        # Keep track of all winners,
        # so that we can have a memory of how well we have been performing
        # Only update the winners queue if the best genome is not already in
        # the winners queue
        if not (max_id in winners_queue_dict):
            winners_queue.append((max_id, max_genome))
            winners_queue_dict[max_id] = 1
            if len(winners_queue) > winner_queue_length:
                to_remove = winners_queue.popleft()[0]
                del winners_queue_dict[to_remove]

        if "debug" in debug and debug["debug"]:
            if "avg" in debug and debug["avg"]:
                avg_move_num = avg_move_num + 0.0
                avg_move_num = avg_move_num / (2 * test_num * len(genomes))
            if "invalid" in debug and debug["invalid"]:
                percent_invalid_move_loss = percent_invalid_move_loss / (2.0 * test_num * len(genomes))
            if "tie" in debug and debug["tie"]:
                percent_tie = percent_tie / (2.0 * test_num * len(genomes))
            if "won" in debug and debug["won"]:
                percent_win = percent_win / (2.0 * test_num * len(genomes))
            if "loss" in debug and debug["loss"]:
                percent_loss = percent_loss / (2.0 * test_num * len(genomes))
            print("################## DEBUG ##################")
            # only check this if we are not doing random sampling
            if "number of games check" in debug and debug["number of games check"]:
                if sample_size == len(genomes):
                    for i in play_track_dict.keys():
                        if not (play_track_dict[i] == 2):
                            print("WARNING: Not all games were played twice")
                            print()

            if "consistent games check" in debug and debug["consistent games check"]:
                if same_pairing_different_result:
                    print("WARNING: Result of games are inconsistent")
                    print("         There seems to be a bug with Neat Python, so this can be a false alarm")
                    print()

            if "show best game" in debug and debug["show best game"]:
                print()
                print("Game Generated by Best AI playing against itself: ")
                create_array_game(
                    [
                        create_player(neat.nn.RecurrentNetwork.create(max_genome, config)),
                        create_player(neat.nn.RecurrentNetwork.create(max_genome, config))
                    ],
                    0
                ).play_game(True)
                print()

            if "show best" in debug and debug["show best"]:
                print('\nBest genome:\n{!s}'.format(max_genome))
                print()

            if "avg" in debug and debug["avg"]:
                print("Average Number of Moves:               "
                      + str(avg_move_num))

            if "max" in debug and debug["max"]:
                print("Max Number of Moves:                   "
                      + str(max_move_num))

            if "invalid" in debug and debug["invalid"]:
                print("Percent of games lost by invalid move: "
                      + str(percent_invalid_move_loss * 100))

            if "won" in debug and debug["won"]:
                print("Percent of games won:                  "
                      + str(percent_win * 100))

            if "loss" in debug and debug["loss"]:
                print("Percent of games lost:                 "
                      + str(percent_loss * 100))

            if "tie" in debug and debug["tie"]:
                print("Percent of games tied:                 "
                      + str(percent_tie * 100))
            print("################# END DEBUG ###############")
            print()

    return eval_genome


# Dummy function for running the population when only the previous winner is wanted
# if elitism is not one this could have weird results
def dummy_eval(genomes, config):
    for genome_id, genome in genomes:
        if genome.fitness is None:
            genome.fitness = -1
