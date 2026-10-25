from base import Heuristic
from puzzle8 import Puzzle8

# 1 2 5         ->          0 1 2
# 3 4 0                     3 4 5
# 6 7 8                     6 7 8

class Manhattan(Heuristic):
    @staticmethod
    def calc(board) -> float:
        distance = 0
        b = board.get_board()

        # Get the minimum number of moves all tiles need to reach goal state
        for value in range(1, 9):
            # Get indexes of current and goal
            ele_index = b.index(value)
            goal_index = Puzzle8.complete_state.index(value)

            # Get the differences between indexes
            # Get x and y coordinates using divmod
            cur_x, cur_y   = divmod(ele_index, 3)
            goal_x, goal_y = divmod(goal_index, 3)

            # Calculate distance
            distance += abs(goal_x - cur_x) + abs(goal_y - cur_y)
    
        return float(distance)