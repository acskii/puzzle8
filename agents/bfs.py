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

    def solve(self):
        start_time = time.time()
        root = Node(self.initial_board)
        max_depth = 0

        if root.state.is_complete():
            return AgentReport([], 0, self.nodes_expanded, 0,
                            time.time() - start_time,
                            states=[root.state],
                            algorithm="Breadth-First Search",
                            max_depth_reached=0)

        self.frontier.append(root)
        self.seen.add(tuple(root.state.get_board()))

        while self.frontier:
            current_node = self.frontier.popleft()

            for child in self._expand(current_node):
                state_tuple = tuple(child.state.get_board())
                if state_tuple in self.seen:
                    continue
                self.seen.add(state_tuple)
                max_depth = max(max_depth, child.depth)

                if child.state.is_complete():
                    actions, states = self.reconstruct_path(child)
                    return AgentReport(
                        path=actions,
                        cost=child.path_cost,
                        nodes_expanded=self.nodes_expanded,
                        search_depth=len(actions),
                        running_time=time.time() - start_time,
                        states=states,
                        algorithm="Breadth-First Search",
                        max_depth_reached=max_depth
                    )

                self.frontier.append(child)

        return AgentReport([], 0, self.nodes_expanded, 0,
                        time.time() - start_time,
                        states=[self.initial_board],
                        algorithm="Breadth-First Search",
                        max_depth_reached=max_depth,
                        solved=False)
