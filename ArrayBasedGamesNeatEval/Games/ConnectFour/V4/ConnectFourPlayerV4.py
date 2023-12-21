from __future__ import annotations

from ArrayBasedGamesNeatEval.Games.ConnectFour.V2.ConnectFourPlayerV2 import ConnectFourPlayerV2


# This player takes in a Connect Four Game state then makes rates all possible next moves
# and makes one
class ConnectFourPlayerV4(ConnectFourPlayerV2):

    # Takes in the current state of a Tic Tac Toe Game and outputs
    # That state converted into a form easier for the AI to understand
    @staticmethod
    def convert_state(player_pos: int, state) -> list[float]:
        opp_pos = (player_pos % 2) + 1

        player_max_count_arr = ConnectFourPlayerV2.in_a_row_count(player_pos, state, 1)

        opp_max_count_arr = ConnectFourPlayerV2.in_a_row_count(opp_pos, state, 0)

        dist_from_center = ConnectFourPlayerV2.avg_distance_from_center(player_pos, state)

        # 0 -> Number of sets of four spaces that include one of my pieces
        #      none of my opponents and all empty spaces are at a parity,
        #      such that they will be naturally claimed by us
        # 1 -> same as 0, but for the opponent
        #
        # 2 -> same as 0, but the sets include two of my pieces
        # 3 -> same as 2, but for the opponent
        #
        # 4 -> same as 0, but the sets include three of my pieces
        # 5 -> same as 4, but for the opponent
        #
        # 6 -> same as 0, but for sets of four of my pieces
        #
        # 7 -> 1 / (x + 1) where x is the avg distance of
        #      my pieces from center column
        feature_list = [
            player_max_count_arr[0] / (player_max_count_arr[0] + 1),
            opp_max_count_arr[0] / (opp_max_count_arr[0] + 1),

            player_max_count_arr[1] / (player_max_count_arr[1] + 1),
            opp_max_count_arr[1] / (opp_max_count_arr[1] + 1),

            player_max_count_arr[2] / (player_max_count_arr[2] + 1),
            opp_max_count_arr[2] / (opp_max_count_arr[2] + 1),

            player_max_count_arr[3] / (player_max_count_arr[3] + 1),

            1.0 / (1.0 + dist_from_center)
        ]
        return feature_list

    # queries player for a move based on state
    def make_move(self, state) -> int:
        player_pos = ConnectFourPlayerV2.determine_turn_order(state)

        move_list = ConnectFourPlayerV2.gen_next_states(player_pos, state)

        feature_move_list = {}
        for i in move_list.keys():
            feature_move_list[i] = ConnectFourPlayerV4.convert_state(
                player_pos,
                move_list[i]
            )
        rating_list = self.rate_states(feature_move_list)

        return ConnectFourPlayerV2.find_max_index(rating_list)
