from unittest import TestCase
import cpmpy as cp

from knsp.problem import ProblemData, ProblemReps
from knsp.models.knsp_1_with_time_intervals import create_model

class Test(TestCase):
    def test_solve_knsp_1_with_time_intervals(self):
        # Example Usage (using data from the MathProg model)
        problem_data: ProblemData = {
            "application_types": ("A1", "A2", "A3"),
            "resource_types": ("CPU", "RAM"),
            "node_types": ("N1", "N2", "N3"),
            "time_intervals": 3,
            "application_requests": (
                (2,2),
                (2,4),
                (6,6),
            ),
            "application_replicas": (
                (2,1,3),
                (3,2,4),
                (2,2,2)
            ),
            "node_capacity": (
                (4,8),
                (8,16),
                (16,32),
            ),
            "node_cost": (10, 19, 28),
            "disruption_budget": 0
        }

        pb = ProblemReps(problem_data)
        model, _, _ = create_model(pb)
        solver = cp.SolverLookup.get("ortools", model)
        solver.solve()

        self.assertEqual(model.objective_value(),171)
