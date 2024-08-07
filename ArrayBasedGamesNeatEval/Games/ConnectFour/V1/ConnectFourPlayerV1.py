from GameInterfaces.IPlayer import IPlayer


# This player takes in a Connect four Game state then makes an optimal move
class ConnectFourPlayerV1(IPlayer):
    _name: str = None
    brain = None

    def __init__(self, brain, name: str = ""):
        self.name = name
        self.brain = brain

    # If this is an AI return true
    # if this is a player don't
    def is_robot(self) -> bool:
        return True

    # Determines whether we went second or first
    @staticmethod
    def determine_turn_order(state) -> int:
        count = 0
        for i in state:
            if not (i == 0):
                count = count + 1
        return (count % 2) + 1

    # Takes in the current state of a Tic Tac Toe Game and outputs
    # That state converted into a form easier for the AI to understand
    @staticmethod
    def convert_state(player_pos: int, state) -> list[int]:
        copy_state = [0 for i in range(126)]

        for i in range(len(state)):
            if state[i] == 0:
                copy_state[i + 84] = 1
            elif player_pos % 2 == 0:
                if state[i] == 1:
                    copy_state[i] = 1
                elif state[i] == 2:
                    copy_state[i + 42] = 1
            else:
                if state[i] == 2:
                    copy_state[i] = 1
                elif state[i] == 1:
                    copy_state[i + 42] = 1
        return copy_state

    # Takes in a list of ints and outputs the index of the maximum value
    @staticmethod
    def find_max_index(val_arr: list[float]) -> int:
        max_val = float('-inf')
        max_index = 0
        for i in range(len(val_arr)):
            if val_arr[i] >= max_val:
                max_val = val_arr[i]
                max_index = i
        return max_index

    # queries player for a move based on state
    def make_move(self, state) -> int:

        output = self.brain.activate(
            ConnectFourPlayerV1.convert_state(
                ConnectFourPlayerV1.determine_turn_order(state),
                state)
        )
        return ConnectFourPlayerV1.find_max_index(output)
