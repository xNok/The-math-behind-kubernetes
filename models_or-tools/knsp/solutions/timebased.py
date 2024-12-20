from ..problem_model import SolutionExtractionInterface

class SolutionExtractorWithReplicasWithTimeIntervals(SolutionExtractionInterface):
    def extract_solution(self, solver, variables, problem_data):
        """Extracts the solution from the solver."""
        optimal_cost = solver.ObjectiveValue()
        x = variables["x"]
        y = variables["y"]

        time_intervals = problem_data["time_intervals"]
        applications = problem_data["applications"]
        replicas = problem_data["replicas"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]
        assignment = {}
        node_counts = {}

        for t in range(time_intervals):
            assignment[t] = {}
            node_counts[t] = {}
            for n in node_types:
                assignment[t][n] = [[] for _ in range(max_nodes[n])]
                node_counts[t][n] = 0
                for i in range(max_nodes[n]):
                    if solver.Value(y[t][n][i]) == 1:
                        node_counts[t][n] += 1
                        for a in applications:
                            for s in range(replicas[a][t]):
                                if solver.Value(x[t][a][s][n][i]) == 1:
                                    assignment[t][n][i].append(a)

        return optimal_cost, assignment, node_counts
