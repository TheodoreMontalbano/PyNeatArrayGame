from __future__ import annotations

from GameInterfaces.IPlayer import IPlayer


class IArrayGame:
    # Current state of the game
    state = None
    players: list[IPlayer] = None
    curr_player: int = None
    move_num: int = None
    invalid_move_loss: bool = None

    # The current player makes a move
    def make_move(self, move):
        pass

    # Has the players play a simulation of the game
    def play_game(self, show: bool = False) -> int:
        pass

    # Checks if the game is over
    def game_state(self):
        pass

    # Outputs the gamestate to the viewer
    def show(self):
        pass
