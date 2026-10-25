from agents.base import BaseAgent
from puzzle8 import Puzzle8, Action
from node import Node
from report import AgentReport
from collections import deque
import time


class BFSAgent(BaseAgent):
    """
    Breadth-First Search (graph search version).
    Expands the shallowest nodes first using a FIFO queue, so with a uniform step
    cost the first goal found is guaranteed to be the shortest solution.
    """

    def __init__(self, initial_board: Puzzle8):
        super().__init__(initial_board)
        # FIFO queue of nodes waiting to be expanded
        self.frontier = deque()
        # States already generated (in frontier or expanded); prevents duplicates and cycles
        self.seen = set()

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
        max_depth = 0

        # Goal test on the root (already solved puzzle)
        if root.state.is_complete():
            return AgentReport([], 0, self.nodes_expanded, max_depth, time.time() - start_time)

        self.frontier.append(root)
        self.seen.add(tuple(root.state.get_board()))

        while self.frontier:
            # Take the oldest node in the queue (shallowest depth)
            current_node = self.frontier.popleft()

            for child in self._expand(current_node):
                state_tuple = tuple(child.state.get_board())

                # Graph search: ignore states that were already generated
                if state_tuple in self.seen:
                    continue
                self.seen.add(state_tuple)
                max_depth = max(max_depth, child.depth)

                # Goal test when the node is generated: for BFS this is safe and saves
                # expanding a whole extra level, and the path is still optimal
                if child.state.is_complete():
                    actions, _ = self.reconstruct_path(child)
                    return AgentReport(
                        path=actions,
                        cost=child.path_cost,
                        nodes_expanded=self.nodes_expanded,
                        search_depth=max_depth,
                        running_time=time.time() - start_time
                    )

                self.frontier.append(child)

        # Frontier is empty and no goal was found (unsolvable puzzle)
        return AgentReport([], 0, self.nodes_expanded, max_depth, time.time() - start_time)
