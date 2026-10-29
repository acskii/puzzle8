from agents.base import BaseAgent
from puzzle8 import Puzzle8, Action
from node import Node
from report import AgentReport
import time


class DFSAgent(BaseAgent):
    """
    Depth-First Search (graph search version).
    Always expands the most recently generated node using a LIFO stack, diving deep
    before backtracking. The explored set prevents infinite loops, so it is complete
    on the finite 8-puzzle state space, but the solution found is NOT necessarily the
    shortest one (it is often very long).
    """

    def __init__(self, initial_board: Puzzle8):
        super().__init__(initial_board)
        # LIFO stack of nodes waiting to be expanded
        self.frontier = []
        # States already expanded; prevents cycles and repeated work
        self.explored = set()

    def solve(self):
        start_time = time.time()
        root = Node(self.initial_board)
        self.frontier.append(root)
        max_depth = 0

        while self.frontier:
            current_node = self.frontier.pop()
            max_depth = max(max_depth, current_node.depth)

            if current_node.state.is_complete():
                actions, states = self.reconstruct_path(current_node)
                return AgentReport(
                    path=actions,
                    cost=current_node.path_cost,
                    nodes_expanded=self.nodes_expanded,
                    search_depth=len(actions),
                    running_time=time.time() - start_time,
                    states=states,
                    algorithm="Depth-First Search (graph search)",
                    max_depth_reached=max_depth
                )

            state_tuple = tuple(current_node.state.get_board())
            if state_tuple in self.explored:
                continue
            self.explored.add(state_tuple)

            for child in reversed(self._expand(current_node)):
                if tuple(child.state.get_board()) not in self.explored:
                    self.frontier.append(child)

        return AgentReport([], 0, self.nodes_expanded, 0,
                        time.time() - start_time,
                        states=[self.initial_board],
                        algorithm="Depth-First Search (graph search)",
                        max_depth_reached=max_depth,
                        solved=False)