from __future__ import annotations

from ArrayBasedGamesNeatEval.Games.ConnectFour.V1.ConnectFourPlayerV1 import ConnectFourPlayerV1
from copy import deepcopy


# This player takes in a Connect Four Game state then makes rates all possible next moves
# and makes one
class ConnectFourPlayerV2(ConnectFourPlayerV1):
    _name: str = None
    brain = None

    # returns how much free the target pieces have around them
    @staticmethod
    def deg_of_freedom(target: int, state) -> float:
        piece_count = 0
        count = 0
        # represents each side we need to check
        deg_arr = [
            [0, 7],
            [0, -7],
            [1, 7],
            [1, -7],
            [-1, -7],
            [-1, 7],
            [1, 0],
            [-1, 0]
        ]
        for i in range(len(state)):
            if state[i] == target:
                piece_count = piece_count + 1
                for j in deg_arr:
                    if 0 <= j[0] + i + j[1] < 42:
                        if state[j[0] + i + j[1]] == 0:
                            count = count + 1
        # Scale by 1/7, since each piece can only have seven free sides at most
        return count / max(piece_count, 1) * 1 / 7

    # returns the average distance of my pieces from the center column
    @staticmethod
    def avg_distance_from_center(target: int, state) -> float:
        sum_dist = 0.0
        count = 0.0
        for i in range(6):
            for j in range(7):
                if state[7 * i + j] == target:
                    sum_dist = sum_dist + abs(3 - j)
                    count = count + 1.0
        return sum_dist / count

    # This function returns the maximum amount in a row
    # in a set that has a potential four in a row ability
    # that a row has
    @staticmethod
    def in_a_row_count(target: int, state) -> float:
        max_count = 0
        max_duplicates = 0
        # i is width, j is height
        for i in range(7):
            for j in range(6):
                up_count = 0
                right_count = 0
                up_diag_count = 0
                low_diag_count = 0
                for k in range(4):
                    # Check up
                    if i + (j + k) * 7 < 42:
                        if state[i + (j + k) * 7] == target:
                            # we have the target present in this set of four
                            up_count = up_count + 1
                        elif not (state[i + (j + k) * 7] == 0):
                            # we cannot get a four in a row on this set of four
                            # set to -10 as that is a number that will stay less
                            # than 0 regardless of increment
                            up_count = -10
                    else:
                        up_count = 0

                    # Check right
                    if i + k < 7:
                        if state[i + k + j * 7] == target:
                            # we have the target present in this set of four
                            right_count = right_count + 1
                        elif not (state[i + k + j * 7] == 0):
                            # we cannot get a four in a row on this set of four
                            # set to -10 as that is a number that will stay less
                            # than 0 regardless of increment
                            right_count = -10
                    else:
                        right_count = 0

                    # Check upper diagonal
                    if i + k < 7 and i + k + (j + k) * 7 < 42:
                        if state[i + k + (j + k) * 7] == target:
                            # we have the target present in this set of four
                            up_diag_count = up_diag_count + 1
                        elif not (state[i + k + (j + k) * 7] == 0):
                            # we cannot get a four in a row on this set of four
                            # set to -10 as that is a number that will stay less
                            # than 0 regardless of increment
                            up_diag_count = -10
                    else:
                        up_diag_count = 0

                    if i == 3 and j == 3:
                        a = 0
                    # Check lower diagonal
                    if i + k < 7 and (j - k) >= 0:
                        if state[i + k + (j - k) * 7] == target:
                            # we have the target present in this set of four
                            low_diag_count = low_diag_count + 1
                        elif not (state[i + k + (j - k) * 7] == 0):
                            # we cannot get a four in a row on this set of four
                            # set to -10 as that is a number that will stay less
                            # than 0 regardless of increment
                            low_diag_count = -10
                    else:
                        low_diag_count = 0
                for k in [up_count, right_count, up_diag_count, low_diag_count]:
                    if k > max_count:
                        max_count = k
                        max_duplicates = 0
                    elif k == max_count > 1:
                        max_duplicates = max_duplicates + 1
        return max_count + max_duplicates / (max_duplicates + 1)

    # Takes in the current state of a Tic Tac Toe Game and outputs
    # That state converted into a form easier for the AI to understand
    @staticmethod
    def convert_state(player_pos: int, state) -> list[float]:
        opp_pos = (player_pos % 2) + 1

        # 0 -> max number of my pieces in a set of 4 that do not include
        #      an opponents piece
        # 1 -> same as 0, but opponents pieces and mine are switched
        # 2 -> 1 / (x + 1) where x is the avg distance of
        #      my pieces from center column
        # 3 -> average amount of free spaces around my pieces
        # 4 -> same as above for opponents
        feature_list = [
            ConnectFourPlayerV2.in_a_row_count(player_pos, state) / 4,
            ConnectFourPlayerV2.in_a_row_count(opp_pos, state) / 4,
            1.0 / (1.0 + ConnectFourPlayerV2.avg_distance_from_center(player_pos, state)),
            ConnectFourPlayerV2.deg_of_freedom(player_pos, state),
            ConnectFourPlayerV2.deg_of_freedom(opp_pos, state)
        ]
        return feature_list

    # Generate all possible states from possible moves we could make
    @staticmethod
    def gen_next_states(player_pos: int, state) -> dict[int, list[int]]:
        to_return = {}
        opp_pos = (player_pos % 2) + 1
        for i in range(7):
            curr_state = ConnectFourPlayerV2.gen_move(player_pos, i, state)
            if not (curr_state is None):
                to_return[i] = curr_state
        return to_return

    # generate state from a move
    @staticmethod
    def gen_move(player_pos: int, move: int, state) -> list[int] | None:
        temp = deepcopy(state)
        # 7 x 6
        for i in range(6):
            if state[move + i * 7] == 0:
                temp[move + i * 7] = player_pos
                return temp
        return None

    # rates all input states
    def rate_states(self, states: dict[int, list[float]]) -> list[float]:
        to_return = [float('-inf') for i in range(7)]
        for i in range(len(to_return)):
            if i in states:
                to_return[i] = self.brain.activate(states[i])[0]
        return to_return

    # queries player for a move based on state
    def make_move(self, state) -> int:
        player_pos = ConnectFourPlayerV1.determine_turn_order(state)

        move_list = ConnectFourPlayerV2.gen_next_states(player_pos, state)

        feature_move_list = {}
        for i in move_list.keys():
            feature_move_list[i] = ConnectFourPlayerV2.convert_state(
                player_pos,
                move_list[i]
            )
        rating_list = self.rate_states(feature_move_list)

        return ConnectFourPlayerV1.find_max_index(rating_list)
