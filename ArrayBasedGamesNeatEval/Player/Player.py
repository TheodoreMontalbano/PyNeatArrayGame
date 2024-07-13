from GameInterfaces.IPlayer import IPlayer


class Player(IPlayer):
    _name: str = None

    def __init__(self, name: str):
        self._name = name

    # If this is an AI return true
    # if this is a player don't
    def is_robot(self) -> bool:
        return False

    # queries player for a move based on state
    def make_move(self, state) -> int:
        return int(input("Please input the move you would like to make "))
