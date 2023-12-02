from ArrayBasedGamesNeatEval.Games.TicTacToe.V2.TicTacToePlayerV2 import TicTacToePlayerV2


# This player takes in a TicTacToe Game state then rates each other possible
# move it could make. Then selects the optimal move with the max score
class TicTacToePlayerV3(TicTacToePlayerV2):

    @staticmethod
    def convert_state(player_pos: int, state) -> list[int]:
        opp_pos = (player_pos % 2) + 1

        # 0 -> max number of my pieces in a row
        # 1 -> max number of opponents pieces in a row
        # 2 -> max amount of empty space around my pieces
        # 3 -> max amount of empty space around opp pieces
        feature_list = [
            TicTacToePlayerV3.num_in_a_row(player_pos, state),
            TicTacToePlayerV3.num_in_a_row(opp_pos, state),
            TicTacToePlayerV3.neighboring_empty(player_pos, state),
            TicTacToePlayerV3.neighboring_empty(opp_pos, state),
        ]

        return feature_list

    # Get the max number in a row of the target piece
    @staticmethod
    def num_in_a_row(target: int, state) -> float:
        opp = (target % 2) + 1
        max_count = 0
        num_of_maxes = 0.0

        # Check Vertical
        for i in range(3):
            count = 0
            for j in range(3):
                if state[i * 3 + j] == target:
                    count = count + 1
                elif state[i * 3 + j] == opp:
                    count = count * 0
                    break
            if count == max_count > 0:
                num_of_maxes = num_of_maxes + 1.0
            elif count > max_count:
                max_count = count
                num_of_maxes = 0.0

        # Check Horizontal
        for i in range(3):
            count = 0
            for j in range(3):
                if state[j * 3 + i] == target:
                    count = count + 1
                elif state[j * 3 + i] == opp:
                    count = count * 0
                    break
            if count == max_count > 0:
                num_of_maxes = num_of_maxes + 1.0
            elif count > max_count:
                max_count = count
                num_of_maxes = 0.0

        # Check Diagonal
        # left to right
        count = 0
        for i in [0, 4, 8]:
            if state[i] == target:
                count = count + 1
            elif state[i] == opp:
                count = count * 0
                break
        if count == max_count > 0:
            num_of_maxes = num_of_maxes + 1.0
        elif count > max_count:
            max_count = count
            num_of_maxes = 0.0

        # right to left
        count = 0
        for i in [2, 4, 6]:
            if state[i] == target:
                count = count + 1
            elif state[i] == opp:
                count = count * 0
                break
        if count == max_count > 0:
            num_of_maxes = num_of_maxes + 1.0
        elif count > max_count:
            max_count = count
            num_of_maxes = 0.0

        return max_count + num_of_maxes / (num_of_maxes + 1)

    # Gets the max amount of neighboring empty space around a target piece
    @staticmethod
    def neighboring_empty(target: int, state) -> int:
        max_count = 0
        for i in range(len(state)):
            count = 0
            if state[i] == target:
                if i % 3 + 1 < 3:
                    # check right
                    if state[i + 1] == 0:
                        count = count + 1
                if i % 3 > 0:
                    # check left
                    if state[i - 1] == 0:
                        count = count + 1
                if (i + 3) < 9:
                    # check up
                    if state[i + 3] == 0:
                        count = count + 1
                if (i - 3) >= 0:
                    # check down
                    if state[i - 3] == 0:
                        count = count + 1
                if i == 4:
                    for j in [0, 2, 6, 8]:
                        if state[j] == 0:
                            count = count + 1
                if i in [0, 2, 6, 8]:
                    if state[4] == 0:
                        count = count + 1
            max_count = max(count, max_count)
        return max_count

    # Player makes a move based on state
    def make_move(self, state) -> int:
        player_pos = TicTacToePlayerV2.determine_turn_order(state)

        move_list = TicTacToePlayerV2.generate_next_states(player_pos, state)
        for i in move_list.keys():
            move_list[i] = TicTacToePlayerV3.convert_state(
                player_pos,
                move_list[i]
            )

        rating_list = self.rate_states(move_list)

        return TicTacToePlayerV2.find_max_index(rating_list)
