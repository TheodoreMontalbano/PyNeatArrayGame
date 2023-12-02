from ArrayBasedGamesNeatEval.GameInterfaces.IPlayer import IPlayer


class MockPlayer(IPlayer):
    _name: str = None
    _move_function = None

    def __init__(self, name: str, moveFunction):
        self._name = name
        self._move_function = moveFunction

    # If this is an AI return true
    # if this is a player don't
    def is_robot(self) -> bool:
        return True

    # queries player for a move based on state
    def make_move(self, state):
        return self._move_function(state)
