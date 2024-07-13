from __future__ import annotations

from Games.ConnectFour.V2.ConnectFourPlayerV2 import ConnectFourPlayerV2


# This player takes in a Connect Four Game state then makes rates all possible next moves
# and makes one
# This AI should not be trained with!!SS
class ConnectFourPlayerV3(ConnectFourPlayerV2):
    _name: str = None
    brain = None

    # recursive helper for making a move
    # returns a states score
    #TODO FIND the bug where some states are present for both players
    def make_move_helper(self,
                         state,
                         player_pos: int,
                         depth_cap: int,
                         memoizer: dict[tuple, float],
                         depth=1
                         ) -> float:
        move_list = ConnectFourPlayerV2.gen_next_states(player_pos, state)
        opp_pos = (player_pos % 2) + 1
        feature_move_list = {}
        for i in move_list.keys():
            feature_move_list[i] = ConnectFourPlayerV2.convert_state(
                player_pos,
                move_list[i]
            )
            if move_list[i] == [2, 2, 2, 1, 2, 1, 0,
                                0, 1, 1, 2, 1, 0, 0,
                                0, 1, 2, 1, 2, 0, 0,
                                0, 0, 0, 1, 1, 0, 0,
                                0, 0, 0, 1, 2, 0, 0,
                                0, 0, 0, 2, 2, 0, 0]:
                print("First_State")
                print(feature_move_list[i])
                print(player_pos)
                print(player_pos == 1)

            if move_list[i] == [2, 2, 2, 1, 2, 1, 0,
                                0, 1, 1, 2, 1, 0, 0,
                                0, 1, 2, 1, 2, 0, 0,
                                0, 0, 1, 1, 1, 0, 0,
                                0, 0, 0, 1, 2, 0, 0,
                                0, 0, 0, 2, 2, 0, 0]:
                print("Second_State")
                print(feature_move_list[i])
                print(player_pos == 2)

            if feature_move_list[i][0] >= 1:
                # Stop recursion as we have already won
                # No better move exists
                return float("inf")
        rating_list = self.rate_states(feature_move_list)
        state_num = len(feature_move_list)
        max_score = float("-inf")
        while state_num > 0:
            curr_index = ConnectFourPlayerV2.find_max_index(rating_list)
            if depth == depth_cap:
                # Stop the recursion and return the max score
                return rating_list[curr_index]
            elif rating_list[curr_index] == float("-inf"):
                return max_score
            else:
                curr_tuple = tuple(move_list[curr_index])
                if curr_tuple in memoizer:
                    curr_score = memoizer[curr_tuple]
                else:
                    curr_score = -1 * self.make_move_helper(
                        move_list[curr_index],
                        opp_pos,
                        depth_cap,
                        memoizer,
                        depth + 1
                    )
                    memoizer[curr_tuple] = curr_score
                if curr_score == float("inf"):
                    return curr_score
                else:
                    max_score = max(curr_score, max_score)
                    state_num = state_num - 1
                    rating_list[curr_index] = float("-inf")
        return max_score

    # queries player for a move based on state
    def make_move(self, state) -> int:
        print(state)
        player_pos = ConnectFourPlayerV2.determine_turn_order(state)
        opp_pos = (player_pos % 2) + 1

        move_list = ConnectFourPlayerV2.gen_next_states(player_pos, state)

        rating_list = [float("-inf") for _ in range(7)]
        d = {}
        for i in move_list.keys():
            rating_list[i] = -1 * self.make_move_helper(
                move_list[i],
                opp_pos,
                6,
                d
            )
        print(rating_list)

        # If everything is negative infinity just try to delay the game
        if max(rating_list) == float("-inf"):
            return ConnectFourPlayerV2(self.brain).make_move(state)

        if max(rating_list) == float("inf"):
            helper = ConnectFourPlayerV2(self.brain)
            to_rate = {}
            for i in range(len(rating_list)):
                if rating_list[i] == float("inf"):
                    to_rate[i] = self.convert_state(player_pos, move_list[i])
            return ConnectFourPlayerV2.find_max_index(self.rate_states(to_rate))

        return ConnectFourPlayerV2.find_max_index(rating_list)
