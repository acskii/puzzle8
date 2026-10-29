from agents.base import BaseAgent
from puzzle8 import Puzzle8
from node import Node
from report import AgentReport
from heuristics.base import Heuristic
import heapq, time

class AStarAgent(BaseAgent):
    def __init__(self, initial_board: Puzzle8, heuristic: Heuristic):
        super().__init__(initial_board)
        self.heuristic = heuristic
        
    def solve(self):
        start_time = time.time()
        
        root = Node(self.initial_board)
        root.h = self.heuristic.calc(root.state)
        root.f = root.path_cost + root.h

        # Initialise data structures
        frontier = []
        heapq.heappush(frontier, (root.f, root))
        explored = set()
        
        max_depth = 0

        while frontier:
            _, current_node = heapq.heappop(frontier)
            
            if current_node.state.is_complete():
                actions, states = self.reconstruct_path(current_node)
                return AgentReport(
                    path=actions,
                    cost=current_node.path_cost,
                    nodes_expanded=self.nodes_expanded,
                    search_depth=len(actions),
                    running_time=time.time() - start_time,
                    states=states,
                    algorithm=f"A* Search ({self.heuristic.__name__})",
                    max_depth_reached=max_depth
                )
            
            state_tuple = tuple(current_node.state.get_board())
            if state_tuple in explored:
                continue
            explored.add(state_tuple)
            
            max_depth = max(max_depth, current_node.depth)

            # If not explored, get expansion of all possible actions to be explored from frontier
            for child in self._expand(current_node):
                if tuple(child.state.get_board()) not in explored:
                    child.h = self.heuristic.calc(child.state)
                    child.f = child.g + child.h
                    heapq.heappush(frontier, (child.f, child))
                    
        # Goal not found
        return AgentReport([], 0, self.nodes_expanded, 0,
                    time.time() - start_time,
                    states=[self.initial_board],
                    algorithm=f"A* Search ({self.heuristic.__name__})",
                    max_depth_reached=max_depth,
                    solved=False
                )