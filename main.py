import random
from puzzle8 import Puzzle8, Action
from agents.bfs import BFSAgent
from agents.dfs import DFSAgent
from agents.a_star import AStarAgent
from heuristics.manhattan import Manhattan
from heuristics.euclidean import Euclidean

_REVERSE = {Action.Up: Action.Down, Action.Down: Action.Up,
            Action.Left: Action.Right, Action.Right: Action.Left}

def random_solvable_board(num_moves: int = 12) -> Puzzle8:
    board = Puzzle8(list(Puzzle8.complete_state))
    last = None
    for _ in range(num_moves):
        choices = [a for a in board.get_possible_actions() if a != _REVERSE.get(last)]
        last = random.choice(choices)
        board = board.move(last)
    return board


if __name__ == "__main__":
    random.seed(42)
    start = random_solvable_board(4)

    print(">>> Random initial state chosen:")
    print(start.pretty())

    experiments = [
        (BFSAgent,  (start,)),
        (DFSAgent,  (start,)),
        (AStarAgent, (start, Manhattan)),
        (AStarAgent, (start, Euclidean)),
    ]

    for cls, args in experiments:
        print(f"\n########## {cls.__name__} ##########")
        agent  = cls(*args)
        report = agent.solve()
        print(report.full_report())