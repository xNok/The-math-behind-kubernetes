from unittest import TestCase

from knsp.problem import ProblemData
from knsp.models.knsp_0_initial_model import solver

class Test(TestCase):
    def test_solve_knsp_0_initial_model(self):
        # Example Usage (using data from the MathProg model)
        problem_data = {
            "application_types": ["A1", "A2", "A3"],
            "resource_types": ["CPU", "RAM"],
            "node_types": ["N1", "N2"],
            "applications_requests": {
                "A1": {"CPU": 2, "RAM": 2},
                "A2": {"CPU": 2, "RAM": 4},
                "A3": {"CPU": 6, "RAM": 6},
            },
            "applications_replicas": {
                "A1": 2,
                "A2": 3,
                "A3": 4,
            },
            "node_capacity": {
                "N1": {"CPU": 4, "RAM": 8},
                "N2": {"CPU": 8, "RAM": 16},
            },
            "node_cost": {"N1": 10, "N2": 19},
        }

        optimal_cost = solver(problem_data)

        self.assertEqual(optimal_cost,29.0)
