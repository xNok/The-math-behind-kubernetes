from unittest import TestCase

from knsp.problem import ProblemData
from knsp.models.knsp_0_initial_model import solver

class Test(TestCase):
    def test_solve_knsp_0_initial_model(self):
        # Example Usage (using data from the MathProg model)
        problem_data: ProblemData = {
            "application_types": ("A1", "A2", "A3"),
            "resource_types": ("CPU", "RAM"),
            "node_types": ("N1", "N2", "N3"),
            "application_requests": (
                (2,2),
                (2,4),
                (6,6),
            ),
            "application_replicas": (2,1,3),
            "node_capacity": (
                (4,8),
                (8,16),
                (16,32),
            ),
            "node_cost": (10, 19, 28),
            "disruption_budget": 0
        }

        optimal_cost, x, y = solver(problem_data)

        self.assertEqual(optimal_cost,57.0)
