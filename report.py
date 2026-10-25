class AgentReport:
    def __init__(self, path, cost, nodes_expanded, search_depth, running_time):
        self.path = path                  # List of Actions or States leading to goal
        self.cost = cost                  # Path cost
        self.nodes_expanded = nodes_expanded
        self.search_depth = search_depth
        self.running_time = running_time  # in seconds

    def __str__(self):
        actions_str = ", ".join([a.name for a in self.path if a])
        return (f"--- Search Report ---\n"
                f"Path to Goal (Actions): [{actions_str}]\n"
                f"Path Cost: {self.cost}\n"
                f"Nodes Expanded: {self.nodes_expanded}\n"
                f"Search Depth: {self.search_depth}\n"
                f"Running Time: {self.running_time:.6f} seconds\n")