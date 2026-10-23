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
        if Puzzle8.verify_board(board): 
            self._board = board
        else:
            print("Initialization of board failed, invalid board. Set to complete state")
            self._board = Puzzle8.complete_state
        
        self._cost = 0

    # Make sure board is valid
    @staticmethod
    def verify_board(board: list):
        return (
            len(board) == 9 and 
            all(0 <= x <= 8 for x in board) and 
            sorted(board) == Puzzle8.complete_state
        )

    # Checks current location of the empty space
    # Then: determines which actions are possible
    #     => if 0 is at start of row -> no left
    #     => if 0 is at end of row -> no right
    #     => if 0 is at start of column -> no up
    #     => if 0 is at end of column -> no down
    def get_possible_actions(self) -> list:
        empty_index: int = self._board.index(0)
        possible_actions: list = [Action.Up, Action.Down, Action.Left, Action.Right]

        if empty_index % 3 == 0:  possible_actions.remove(Action.Left) # Remove left
        if empty_index % 3 == 2:  possible_actions.remove(Action.Right) # Remove right
        if 0 <= empty_index <= 2: possible_actions.remove(Action.Up) # Remove up
        if 6 <= empty_index <= 8: possible_actions.remove(Action.Down) # Remove down

        return possible_actions

    # Moves empty space based on given action
    # Only allows valid actions based on current board state
    # Return instance of new board state
    def move(self, action: Action) -> Puzzle8:
        possible_action: list = self.get_possible_actions()

        try:
            if possible_action.index(action):
                empty_index: int = self._board.index(0)
                new_board = self._board
                match action:
                    # Swap empty space with spot 3 indexes away
                    case Action.Up:
                        new_board[empty_index], new_board[empty_index - 3] = new_board[empty_index - 3], new_board[empty_index]

                    case Action.Down:
                        new_board[empty_index], new_board[empty_index + 3] = new_board[empty_index + 3], new_board[empty_index]

                    # Swap empty space with spot before or after
                    case Action.Left:
                        new_board[empty_index], new_board[empty_index - 1] = new_board[empty_index - 1], new_board[empty_index]
                    
                    case Action.Right:
                        new_board[empty_index], new_board[empty_index + 1] = new_board[empty_index + 1], new_board[empty_index]

                return Puzzle8(new_board)

        except ValueError:
            print("Attempted to move empty space with invalid action at current state, no moves done")
            return

    def get_board(self):
        return self._board

    # Check if board has reached complete state
    def is_complete(self):
        return self._board == Puzzle8.complete_state

    # Check if both instances are equal states
    def __eq__(self, other):
        return isinstance(other, Puzzle8) and self._board == other.get_board()

    # Used to add instance in sets
    def __hash__(self):
        return hash(tuple(self._board))

    def __str__(self):
        t = [str(x) for x in self._board]
        return ", ".join(t)