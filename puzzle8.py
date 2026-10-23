from enum import Enum

# Enum that holds all possible actions that empty space can do
class Action(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

class Puzzle8:
    # Default the completed state of the puzzle board
    complete_state: list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self, board: list):
        if self._verify_board(board): 
            self._board = board
            self._complete = False
        else:
            print("Initialization of board failed, invalid board. Set to complete state")
            self._board = Puzzle8.complete_state
            self._complete = True
        
        self._cost = 0

    # Make sure board is valid
    def _verify_board(board: list):
        return len(board) == 9 and all(0 <= x <= 8 for x in board)

    def get_possible_actions(self):
        return

    def move(self, action: Action):
        pass

    def get_cost(self):
        return self._cost

    def get_board(self):
        return self._board

    def is_complete(self):
        return self._complete

    def __str__(self):
        return ", ".join(self._board)