from unittest import TestCase
from knsp.problem import ProblemData
from knsp.models.knsp_0_initial_model import solver

class Test(TestCase):
    def test_solve_0_knsp(self):
        # Example Usage (using data from the MathProg model)
        problem_data = {
            "applications": ["A1", "A2", "A3"],
            "resources": ["CPU", "RAM"],
            "node_types": ["N1", "N2"],
            "applications_requests": {
                "A1": {"CPU": 2, "RAM": 2},
                "A2": {"CPU": 2, "RAM": 4},
                "A3": {"CPU": 6, "RAM": 6},
            },
            "node_capacity": {
                "N1": {"CPU": 4, "RAM": 8},
                "N2": {"CPU": 8, "RAM": 16},
            },
            "node_cost": {"N1": 10, "N2": 19},
        }

        optimal_cost, assignment, node_counts = solver(problem_data)

        assert optimal_cost == 29.0


