class AgentReport:
    def __init__(self, path, cost, nodes_expanded, search_depth, running_time, states = None, algorithm = "", 
                 max_depth_reached = None, solved = True):
        self.path              = path                 # list[Action]
        self.cost              = cost                 # int (steps)
        self.nodes_expanded    = nodes_expanded
        self.search_depth      = search_depth         # depth of goal node (= len(path))
        self.running_time      = running_time
        self.states            = states or []         # list[Puzzle8] initial → goal
        self.algorithm         = algorithm
        self.max_depth_reached = max_depth_reached if max_depth_reached is not None else search_depth
        self.solved            = solved

    # -------- summary block --------
    def __str__(self):
        actions_str = ", ".join(a.name for a in self.path) or "(none)"
        return (
            f"Search Report       : {self.algorithm}\n"
            f"Solution found      : {self.solved}\n"
            f"Path to goal        : [{actions_str}]\n"
            f"Path cost           : {self.cost}\n"
            f"Nodes expanded      : {self.nodes_expanded}\n"
            f"Search depth (goal) : {self.search_depth}\n"
            f"Max depth reached   : {self.max_depth_reached}\n"
            f"Running time        : {self.running_time:.6f} s\n"
        )

    # -------- step-by-step trace --------
    def trace(self) -> str:
        if not self.states:
            return "(no states recorded)\n"

        out = ["-" * 60, "Step-by-step trace", "-" * 60,
               "Initial state:", self.states[0].pretty()]

        if not self.solved:
            out.append("No solution found (frontier exhausted — puzzle is unsolvable).\n")
            return "\n".join(out)

        if not self.path:                       # already at goal
            out.append("Initial state is already the goal state.\n")
            return "\n".join(out)

        for i, (action, state) in enumerate(zip(self.path, self.states[1:]), start=1):
            out.append(f"Step {i}: move {action.name}")
            out.append(state.pretty())

        out.append(f"Goal reached in {len(self.path)} steps (cost = {self.cost}).\n")
        return "\n".join(out)

    def full_report(self) -> str:
        return self.__str__() + "\n" + self.trace()