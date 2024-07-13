from __future__ import annotations

from Games.ConnectFour.V1.ConnectFourPlayerV1 import ConnectFourPlayerV1
from copy import deepcopy


# This player takes in a Connect Four Game state then makes rates all possible next moves
# and makes one
class ConnectFourPlayerV2(ConnectFourPlayerV1):

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

    @staticmethod
    def get_height_counts(state) -> list[int]:
        to_ret = [0 for i in range(7)]
        for i in range(7):
            while (i + 7 * to_ret[i] < 42 and
                   not (state[i + 7 * to_ret[i]] == 0)):
                to_ret[i] = to_ret[i] + 1
        return to_ret

    # This function returns the maximum amount in a row
    # in a set that has a potential four in a row ability
    # that a row has
    @staticmethod
    def in_a_row_count(target: int, state, parity: int) -> list[int]:
        height_counts = ConnectFourPlayerV2.get_height_counts(state)
        in_a_row_count = [0 for _ in range(4)]

        # i is width, j is height
        for i in range(7):
            for j in range(6):
                up_count = 0
                right_count = 0
                up_diag_count = 0
                low_diag_count = 0
                if i == 1 and j == 0:
                    a = 0
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
                        elif not ((j + k - height_counts[i]) % 2 == parity):
                            # Only count the set if we will naturally get the set
                            # We naturally get the set if we are an even parity away
                            # from it
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
                        elif not ((j - height_counts[i + k]) % 2 == parity):
                            # Only count the set if we will naturally get the set
                            # We naturally get the set if we are an even parity away
                            # from it
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
                        elif not ((j + k - height_counts[i + k]) % 2 == parity):
                            # Only count the set if we will naturally get the set
                            # We naturally get the set if we are an even parity away
                            # from it
                            up_diag_count = -10
                    else:
                        up_diag_count = 0

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
                        elif not ((j - k - height_counts[i + k]) % 2 == parity):
                            # Only count the set if we will naturally get the set
                            # We naturally get the set if we are an even parity away
                            # from it
                            low_diag_count = -10
                    else:
                        low_diag_count = 0
                for k in [up_count, right_count, up_diag_count, low_diag_count]:
                    if k > 0:
                        in_a_row_count[k - 1] = in_a_row_count[k - 1] + 1
        return in_a_row_count

    # Takes in the current state of a Tic Tac Toe Game and outputs
    # That state converted into a form easier for the AI to understand
    @staticmethod
    def convert_state(player_pos: int, state) -> list[float]:
        opp_pos = (player_pos % 2) + 1

        # Computes the max in a row count present in the given array.
        # Array is assumed to have a structure such that arr[i] is the
        # amount of sets of size i + 1 "in a row" that are in the board
        def compute_max_count(arr: list[int]) -> float:
            max_count = 0
            for i in range(len(arr)):
                if not arr[i] == 0:
                    max_count = (i + 1) * (arr[i] / (arr[i] + 1))
            return max_count

        player_max_count = compute_max_count(ConnectFourPlayerV2.in_a_row_count(player_pos, state, 1))

        opp_max_count = compute_max_count(ConnectFourPlayerV2.in_a_row_count(opp_pos, state, 0))

        dist_from_center = ConnectFourPlayerV2.avg_distance_from_center(player_pos, state)

        # 0 -> max number of my pieces in a set of 4 that do not include
        #      an opponents piece (normalized). The set of four must also
        #      be an odd parity away
        # 1 -> same as 0, but opponents pieces and mine are switched
        # 2 -> 1 / (x + 1) where x is the avg distance of
        #      my pieces from center column
        feature_list = [
            player_max_count / 4,
            opp_max_count / 4,
            1.0 / (1.0 + dist_from_center)
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
