from IPlayer import IPlayer
from IArrayGame import IArrayGame

class INNPlayer(IPlayer):
    # The Name of this NN
    _name: str = None
    # The brain the NN requires to play this game
    _brain = None

    # region Inherited methods

    # Returns the name of this AI
    def get_name(self) -> str:
        return self._name

    # If this is an AI return true
    # if this is a player don't
    def is_robot(self) -> bool:
        return True

    # endregion

    # region Methods needing implementation

    # Returns the name of the game
    @staticmethod
    def get_game_name() -> str:
        pass

    # queries player for a move based on state
    def make_move(self, state):
        pass

    # Returns the game that this NN is meant to be trained on
    @staticmethod
    def get_game() -> IArrayGame:
        pass

    # Returns list of basic players for guidance for AI
    # Only necessary if you want to use launchpad of genetic alg
    @staticmethod
    def get_launch_pad_players() -> list[IPlayer]:
        pass
    # endregion
