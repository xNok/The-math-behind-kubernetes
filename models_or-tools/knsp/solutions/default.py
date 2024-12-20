from ..problem_model import SolutionExtractionInterface

class DefaultSolutionExtractor(SolutionExtractionInterface):
    def extract_solution(self, solver, variables, problem_data):
        """Extracts the solution from the solver."""
        optimal_cost = solver.ObjectiveValue()
        x = variables["x"]
        y = variables["y"]
        applications = problem_data["applications"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]
        assignment = {}
        node_counts = {}
        for n in node_types:
            assignment[n] = [[] for _ in range(max_nodes[n])]
            node_counts[n] = 0
            for i in range(max_nodes[n]):
                if solver.Value(y[n][i]) == 1:
                    node_counts[n] += 1
                    for a in applications:
                        if solver.Value(x[a][n][i]) == 1:
                            assignment[n][i].append(a)

        return optimal_cost, assignment, node_counts
