from unittest import TestCase

from knsp.models.knsp_2_auto_scaling import solve_2_knsp


class Test(TestCase):
    def test_solve_2_knsp(self):
        # Example Usage (using data from the MathProg model)
        problem_data = {
            "applications": ["A1", "A2", "A3"],
            "resources": ["CPU", "RAM"],
            "node_types": ["N1", "N2", "N3"],
            "time_intervals": 3,
            "replicas": {
                "A1": [2, 3, 2],
                "A2": [2, 5, 3],
                "A3": [3, 3, 2],
            },
            "r": {
                "A1": {"CPU": 2, "RAM": 2},
                "A2": {"CPU": 2, "RAM": 4},
                "A3": {"CPU": 6, "RAM": 6},
            },
            "c": {
                "N1": {"CPU": 4, "RAM": 8},
                "N2": {"CPU": 8, "RAM": 16},
                "N3": {"CPU": 16, "RAM": 32},
            },
            "cost": {"N1": 10, "N2": 19, "N3": 28},
        }

        optimal_cost, assignment, node_counts = solve_2_knsp(problem_data)

        assert optimal_cost == 212.0

        if optimal_cost is not None:
            print(f"Total cost: {optimal_cost}")
            for t in range(problem_data["time_intervals"]):
                print(f"----- t{t} -----")
                for n in problem_data["node_types"]:
                    print(f"Nodes of type {n} used: {node_counts[t][n]}")
                    for i, apps in enumerate(assignment[t][n]):
                        if apps:
                            print(f"  Node {i + 1}: {', '.join(apps)}")
        else:
            print("No feasible solution found.")
