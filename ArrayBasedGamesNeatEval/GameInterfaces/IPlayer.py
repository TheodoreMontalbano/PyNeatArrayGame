class IPlayer:
    _name: str = None

    # If this is an AI return true
    # if this is a player don't
    def is_robot(self) -> bool:
        pass

    # queries player for a move based on state
    def make_move(self, state):
        pass

    def get_name(self) -> str:
        return self._name
