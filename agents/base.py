from puzzle8 import Puzzle8, Action
from node import Node
from abc import ABC, abstractmethod

# Use this base class to create other agents
# e.g. class BFSAgent(BaseAgent):
#          .. other methods needed ..
#          .. add data structures here .. (Queue for BFS)
#          def solve(self):
#              """ Implementation here """ 

class BaseAgent(ABC):
    def __init__(self, initial_board: Puzzle8):
        self.initial_board = initial_board
        self.nodes_expanded = 0

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

    # Trace back the goal path to the root, and return the actions taken and the states 
    # that were passed through to reach it
    def reconstruct_path(self, node: Node) -> tuple[list, list]:
        actions = []
        states = [node.state]
        current = node
        while current.parent is not None:
            actions.append(current.action)
            states.append(current.parent.state)
            current = current.parent
        actions.reverse()
        states.reverse()
        return actions, states

    @abstractmethod
    def solve(self):
        pass