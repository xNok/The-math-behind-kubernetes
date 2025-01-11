from unittest import TestCase

from knsp.problem import ProblemData
from knsp.models.knsp_0_initial_model import solver

class Test(TestCase):
    def test_solve_knsp_0_initial_model(self):
        # Example Usage (using data from the MathProg model)
        problem_data: ProblemData = {
            "application_types": ("A1", "A2", "A3"),
            "resource_types": ("CPU", "RAM"),
            "node_types": ("N1", "N2"),
            "applications_requests": (
                (1,2),
                (2,4),
                (6,6),
            ),
            "applications_replicas": (2,3,4),
            "node_capacity": (
                (4,8),
                (8,16),
            ),
            "node_cost": (10, 19),
        }

        optimal_cost = solver(problem_data)

        self.assertEqual(optimal_cost,29.0)
