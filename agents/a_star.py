from base import BaseAgent
from puzzle8 import Puzzle8, Action
from heuristics.base import Heuristic

class AStarAgent(BaseAgent):
    def __init__(self, initial_board: Puzzle8, heuristic: Heuristic):
        super(initial_board)
        self.heuristic = heuristic
        # Initialise data structure and other attributes here
        
    def solve(self):
        # Add implementation here
        pass