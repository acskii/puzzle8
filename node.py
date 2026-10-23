# Used to keep track of board states for agent search
# Stores parent and current board state
#        action that led to current state
#        path cost accumulated g(n)
#        depth of search tree
#        heurestic value h(n)
#        For A* = g(n) + h(n)

from puzzle8 import Puzzle8, Action

class Node:
    def __init__(self, state: Puzzle8, parent: Node = None, action: Action = None, path_cost = 0, depth = 0):
        self.state = state          # Current board state
        self.parent = parent        # Parent node
        self.action = action        # Action taken from parent to reach this state
        self.path_cost = path_cost  # Cost to reach this node
        self.depth = depth          # Search depth
        self.g = path_cost          # Cost so far (for A*)
        self.h = 0                  # Heuristic value (for A*)
        self.f = 0                  # Total estimated cost (g + h)

    # Comparison function for heapsort
    def __lt__(self, other):
        return self.f < other.f