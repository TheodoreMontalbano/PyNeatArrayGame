from __future__ import annotations

import random
from ArrayBasedGamesNeatEval.Enums.GameState import GameState
from ArrayBasedGamesNeatEval.Enums.InvalidMoveCases import InvalidMoveCases
from ArrayBasedGamesNeatEval.GameInterfaces.IPlayer import IPlayer
from ArrayBasedGamesNeatEval.GameInterfaces.IArrayGame import IArrayGame


class TicTacToe(IArrayGame):
    # Current state of the game
    state: list[int] | None = None
    players: list[IPlayer] | None = None
    curr_player: int | None = None
    move_num: int = 0
    invalid_move_loss = False
    starting_player = None

    def __init__(self, players: list[IPlayer], starting_player: int | None):
        self.players = players
        if not (starting_player is None):
            self.curr_player = starting_player
            self.starting_player = starting_player
        else:
            self.curr_player = random.randint(0, 1)
            self.starting_player = self.curr_player
        self.state = [0 for i in range(9)]

    @staticmethod
    def player_invalid_move_message():
        print("Invalid Move: Here are a refresher of the rules")
        print("Moves must be a number between 0 and 8")
        print("The board is represented as follows:")
        print("0 1 2")
        print("3 4 5")
        print("6 7 8")
        print("You cannot go where a player has already gone")
        print("Please input a valid move")

    @staticmethod
    def translate(i: int) -> str:
        if i == 0:
            return " "
        elif i == 1:
            return "X"
        elif i == 2:
            return "O"

    # region Overriden/Implemented methods

    # The current player makes a move
    def make_move(self, move: int) -> InvalidMoveCases:
        if 0 <= move < 9 and self.state[move] == 0:
            if self.starting_player == self.curr_player:
                self.state[move] = 1
            else:
                self.state[move] = 2
            return InvalidMoveCases.ValidMove
        else:
            if self.players[self.curr_player].is_robot():
                return InvalidMoveCases.AIInvalid
            else:
                return InvalidMoveCases.PlayerInvalid

    # Has the players play a simulation of the game
    # Returns the index of the winning player + 1
    # Returns 0 in the case of a tie
    def play_game(self, show=False) -> int:
        curr_state = GameState.NotOver
        while curr_state == GameState.NotOver:
            move_case = InvalidMoveCases.PlayerInvalid
            while move_case == InvalidMoveCases.PlayerInvalid:
                move_case = (
                    self.make_move(
                        self.players[self.curr_player].make_move(self.state)))
                if move_case == InvalidMoveCases.AIInvalid:
                    # AI automatically loses if making an invalid move
                    self.invalid_move_loss = True
                    return (self.curr_player + 1) % 2 + 1
                elif move_case == InvalidMoveCases.PlayerInvalid:
                    # Give the player a chance to do the correct move
                    TicTacToe.player_invalid_move_message()
                if show:
                    self.show()
            self.move_num = self.move_num + 1
            curr_state = self.game_state()
            if curr_state == GameState.Win:
                return self.curr_player + 1
            elif curr_state == GameState.Tie:
                return 0
            self.curr_player = (self.curr_player + 1) % 2
        return 0

    # Checks if the game is over
    def game_state(self) -> GameState:
        to_return = GameState.Tie
        for i in self.state:
            if i == 0:
                to_return = GameState.NotOver
        # Check Vertical
        for i in range(3):
            if not self.state[i] == 0:
                if self.state[i] == self.state[i + 3] == self.state[i + 6]:
                    return GameState.Win
        # Check Horizontal
        for i in [0, 3, 6]:
            if not self.state[i] == 0:
                if self.state[i] == self.state[i + 1] == self.state[i + 2]:
                    return GameState.Win
        # Check Diagonal
        # left to right
        if self.state[0] == self.state[4] == self.state[8] and not (self.state[0] == 0):
            return GameState.Win
        # right to left
        if self.state[2] == self.state[4] == self.state[6] and not (self.state[2] == 0):
            return GameState.Win
        return to_return

    # Outputs the game state to the console
    def show(self):
        for i in range(3):
            for j in range(2):
                print(TicTacToe.translate(self.state[i * 3 + j]), end=' | ')
            print(TicTacToe.translate(self.state[i * 3 + 2]))
            if i < 2:
                print("----------")
        print()

    # endregion
