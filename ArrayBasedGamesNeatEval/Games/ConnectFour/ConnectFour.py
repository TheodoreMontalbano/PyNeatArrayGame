from GameInterfaces.IArrayGame import IArrayGame
from copy import deepcopy
from Enums.GameState import GameState
from Enums.InvalidMoveCases import InvalidMoveCases
from GameInterfaces.IPlayer import IPlayer
import math


class ConnectFour(IArrayGame):
    # Current state of the game
    state: list[list[int]] = None
    state_vector: list[int] = None
    players: list[IPlayer] = None
    curr_player: int = None
    move_num: int = 0
    invalid_move_loss: bool = False
    curr_empty = None
    starting_player: int = None

    def __init__(self, players: list[IPlayer], starting_player=0):
        # 6 row, 7 col
        temp = [0 for i in range(6)]
        self.state = [deepcopy(temp) for i in range(7)]
        self.state_vector = [0 for i in range(42)]
        self.players = players
        self.curr_player = starting_player
        self.starting_player = starting_player
        self.curr_empty = [0 for i in range(7)]

    # The current player makes a move
    def make_move(self, move):
        if 0 > move or move > 6 or self.curr_empty[move] == 6:
            if self.players[self.curr_player].is_robot():
                return InvalidMoveCases.AIInvalid
            else:
                return InvalidMoveCases.PlayerInvalid
        self.state[move][self.curr_empty[move]] = (self.curr_player + self.starting_player) % 2 + 1
        self.state_vector[move + self.curr_empty[move] * 7] = (self.curr_player + self.starting_player) % 2 + 1
        self.curr_empty[move] = self.curr_empty[move] + 1
        return InvalidMoveCases.ValidMove

    # Has the players play a simulation of the game
    def play_game(self, show_game=False):
        is_over = GameState.NotOver
        while is_over == GameState.NotOver:
            # Make a move
            move = self.players[self.curr_player].make_move(self.state_vector)
            if math.isnan(move):
                move = -1
            else:
                move = int(move)
            move_validity = self.make_move(move)
            while move_validity == InvalidMoveCases.PlayerInvalid:
                if 0 > move or move > 6:
                    print("Invalid move: please choose a number between 1 and 7")
                else:
                    print("Invalid move: Please choose a column that is not full")
                move_validity = self.make_move(self.players[self.curr_player].make_move(self.state))
            # If the AI makes an invalid move it counts as a loss
            if move_validity == InvalidMoveCases.AIInvalid:
                self.invalid_move_loss = True
                return (self.curr_player + 1) % 2 + 1
            if show_game:
                self.show()
            is_over = self.game_state()
            if is_over == GameState.Win:
                return self.curr_player + 1
            elif is_over == GameState.Tie:
                return 0
            self.curr_player = (self.curr_player + 1) % 2
            self.move_num = self.move_num + 1

    # Checks if the game is over
    def game_state(self):
        if self._check_horizontal() or self._check_vertical() or self._check_diagonal():
            return GameState.Win

        i = 0
        is_tie = True
        while i < 7 and is_tie:
            if self.curr_empty[i] != 6:
                is_tie = False
            i = i + 1
        if is_tie:
            return GameState.Tie
        else:
            return GameState.NotOver

    # Checks the horizontals of the board for a win
    def _check_horizontal(self):
        is_win = False
        for i in range(6):
            count = 0
            for j in range(6):
                if self.state[j][i] == self.state[j + 1][i] and self.state[j][i] != 0:
                    count = count + 1
                    if count == 3:
                        is_win = True
                else:
                    count = 0
        return is_win

    # Checks the verticals of the board for a win
    def _check_vertical(self):
        is_win = False
        for i in range(7):
            count = 0
            for j in range(5):
                if self.state[i][j] == self.state[i][j + 1] and self.state[i][j] != 0:
                    count = count + 1
                    if count == 3:
                        is_win = True
                else:
                    count = 0
        return is_win

    # Checks the diagonals of the board for a win
    def _check_diagonal(self):
        is_win = False
        # Upper 1/1 diagonal
        for i in range(4):
            count = 0
            for j in range(i, 5):
                if self.state[j - i][j] == self.state[j + 1 - i][j + 1] and self.state[j - i][j] != 0:
                    count = count + 1
                    if count == 3:
                        is_win = True
                else:
                    count = 0
        # Lower 1/1 diagonal
        for i in range(1, 4):
            count = 0
            for j in range(i, 6):
                if self.state[j][j - i] == self.state[j + 1][j - i + 1] and self.state[j][j - i] != 0:
                    count = count + 1
                    if count == 3:
                        is_win = True
                else:
                    count = 0
        # Upper -1/1 diagonal
        for i in range(4):
            count = 0
            for j in range(i, 5):
                if self.state[6 - (j - i)][j] == self.state[6 - (j + 1 - i)][(j + 1)] \
                        and self.state[6 - (j - i)][j] != 0:
                    count = count + 1
                    if count == 3:
                        is_win = True
                else:
                    count = 0
        # Lower -1/1 diagonal
        for i in range(1, 4):
            count = 0
            for j in range(i, 6):
                if self.state[6 - j][(j - i)] == self.state[6 - (j + 1)][j - i + 1] and self.state[6 - j][j - i] != 0:
                    count = count + 1
                    if count == 3:
                        is_win = True
                else:
                    count = 0
        return is_win

    # Outputs the game's state to the viewer
    def show(self):
        print()
        for i in range(1, 7):
            for j in range(7):
                print('{:3}'.format(translate(self.state[j][6 - i])), end='')
            print()
        print()


def translate(x):
    if x == 1:
        return 'R'
    if x == 2:
        return 'B'
    return '_'
