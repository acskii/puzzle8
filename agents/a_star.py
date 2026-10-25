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
        
    # Get all children from a board state based on possible actions from that state
    def _expand(self, node: Node) -> list:
        self.nodes_expanded += 1
        children = []
        for action in node.state.get_possible_actions():
            next_state = node.state.move(action)
            child_node = Node(
                state = next_state,
                parent = node,
                action = action,
                path_cost = node.path_cost + 1,
                depth = node.depth + 1
            )
            children.append(child_node)
        return children
    
    def solve(self):
        start_time = time.time()
        
        root = Node(self.initial_board)
        root.h = self.heuristic.calc(root.state)
        root.f = root.g + root.h

        # Initialise data structures
        frontier = []
        heapq.heappush(frontier, (root.f, root))
        explored = set()
        
        max_depth = 0

        while frontier:
            _, current_node = heapq.heappop(frontier)
            
            if current_node.state.is_complete():
                running_time = time.time() - start_time
                actions, _ = self.reconstruct_path(current_node)
                return AgentReport(
                    path = actions,
                    cost = current_node.path_cost,
                    nodes_expanded = self.nodes_expanded,
                    search_depth = max_depth,
                    running_time = running_time
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
                    
        running_time = time.time() - start_time
        # Goal not found
        return AgentReport([], 0, self.nodes_expanded, max_depth, running_time)