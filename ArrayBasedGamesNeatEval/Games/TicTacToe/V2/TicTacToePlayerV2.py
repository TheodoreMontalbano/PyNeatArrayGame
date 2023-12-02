from ArrayBasedGamesNeatEval.Games.TicTacToe.V1.TicTacToePlayer import TicTacToePlayer
from copy import deepcopy


# This player takes in a TicTacToe Game state then rates each other possible
# move it could make. Then selects the optimal move with the max score
class TicTacToePlayerV2(TicTacToePlayer):

    # Generates all possible states based on the next move a player makes
    @staticmethod
    def generate_next_states(player_pos, state) -> dict[int, list[int]]:
        to_return = {}
        temp = []
        for i in range(len(state)):
            if state[i] == 0:
                temp = deepcopy(state)
                temp[i] = player_pos
                to_return[i] = temp
        return to_return

    # rates all input states
    def rate_states(self, states: dict[int, list[int]]) -> list[float]:
        to_return = [float('-inf') for i in range(9)]
        for i in range(len(to_return)):
            if i in states:
                to_return[i] = self.brain.activate(states[i])[0]
        return to_return

    # Player makes a move based on state
    def make_move(self, state) -> int:
        player_pos = TicTacToePlayer.determine_turn_order(state)

        move_list = TicTacToePlayerV2.generate_next_states(player_pos, state)
        for i in move_list.keys():
            move_list[i] = TicTacToePlayer.convert_state(
                player_pos,
                move_list[i]
            )

        rating_list = self.rate_states(move_list)

        return TicTacToePlayer.find_max_index(rating_list)
