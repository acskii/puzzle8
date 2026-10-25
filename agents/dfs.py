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

    # Get all children from a board state based on possible actions from that state
    def _expand(self, node: Node) -> list:
        self.nodes_expanded += 1
        children = []
        for action in node.state.get_possible_actions():
            children.append(Node(
                state=node.state.move(action),
                parent=node,
                action=action,
                path_cost=node.path_cost + 1,
                depth=node.depth + 1
            ))
        return children

    def solve(self):
        start_time = time.time()

        root = Node(self.initial_board)
        self.frontier.append(root)
        max_depth = 0

        while self.frontier:
            # Take the newest node on the stack (deepest so far)
            current_node = self.frontier.pop()
            max_depth = max(max_depth, current_node.depth)

            # Goal test when the node is taken from the stack
            if current_node.state.is_complete():
                actions, _ = self.reconstruct_path(current_node)
                return AgentReport(
                    path=actions,
                    cost=current_node.path_cost,
                    nodes_expanded=self.nodes_expanded,
                    search_depth=max_depth,
                    running_time=time.time() - start_time
                )

            # The same state can be pushed more than once before it is popped,
            # so skip it here if it was already expanded
            state_tuple = tuple(current_node.state.get_board())
            if state_tuple in self.explored:
                continue
            self.explored.add(state_tuple)

            # Push children that were not expanded yet; the last one pushed is explored first
            for child in reversed(self._expand(current_node)):
                if tuple(child.state.get_board()) not in self.explored:
                    self.frontier.append(child)

        # Stack is empty and no goal was found (unsolvable puzzle)
        return AgentReport([], 0, self.nodes_expanded, max_depth, time.time() - start_time)
