from puzzle8 import Puzzle8
from abc import ABC, abstractmethod

class Heuristic(ABC):
    @staticmethod
    @abstractmethod
    def calc(board: Puzzle8):
        pass

# Use this base class to implement heuristics needed
# Just implement calc() function
# e.g. class Manhattan(Heuristic):
#          def calc(board: Puzzle8):
#              """ Implementation here """ 
#
# Then A* agent can call Heuristic.calc(board) and you can inject either Manhattan or Euclidean must on run