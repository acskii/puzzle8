from agents.base import BaseAgent
from puzzle8 import Puzzle8, Action
from node import Node
from report import AgentReport
import time


class IDFSAgent(BaseAgent):
    # Search the puzzle with iterative deepening DFS.
    # Increase the depth limit until the goal is found.
    # For unit step costs, this finds a shortest solution.
    # It uses less memory than breadth-first search.
    # Nodes at shallow depths are searched again on later passes.
    # Cycle checking uses only the current path.

    def __init__(self, initial_board: Puzzle8):
        super().__init__(initial_board)

    # a 3x3 puzzle is solvable when its inversion count is even.
    def _is_solvable(self) -> bool:
        tiles = [tile for tile in self.initial_board.get_board() if tile != 0]
        inversions = sum(
            1
            for i in range(len(tiles))
            for j in range(i + 1, len(tiles))
            if tiles[i] > tiles[j]
        )
        return inversions % 2 == 0
    
    # cycle check whether this state is already on the current path.
    def _on_path(self, node: Node, state: Puzzle8) -> bool:
        while node is not None:
            if node.state == state:
                return True
            node = node.parent

        return False

    # search up to the given depth limit.
    def _depth_limited(self, limit: int):
        frontier = [Node(self.initial_board)]

        while frontier:
            current_node = frontier.pop()

            if current_node.state.is_complete():
                return current_node

            if current_node.depth < limit:
                # reverse children so the first action is searched first.
                for child in reversed(self._expand(current_node)):
                    if not self._on_path(current_node, child.state):
                        frontier.append(child)

        return None

    def solve(self):
        start_time = time.time()

        # Unsolvable board: return a report flagged as not solved.
        # states holds just the initial board so trace() can still print it.
        if not self._is_solvable():
            return AgentReport(
                path=[],
                cost=0,
                nodes_expanded=0,
                search_depth=0,
                running_time=time.time() - start_time,
                states=[self.initial_board],
                algorithm="Iterative Deepening DFS",
                solved=False,
            )

        self.nodes_expanded = 0
        limit = 0

        while True:
            goal = self._depth_limited(limit)

            if goal is not None:
                # Keep the states list instead of discarding it with "_"
                actions, states = self.reconstruct_path(goal)
                return AgentReport(
                    path=actions,
                    cost=goal.path_cost,
                    nodes_expanded=self.nodes_expanded,
                    search_depth=goal.depth,
                    running_time=time.time() - start_time,
                    states=states,
                    algorithm="Iterative Deepening DFS",
                )

            limit += 1