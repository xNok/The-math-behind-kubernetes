from knsp.problem_factory import ProblemFactory
from knsp.problem_model import ProblemData
from knsp.variables.application_placement import ApplicationReplicasPlacementVariables
from knsp.variables.node_selection import NodeSelectionVariables
from knsp.constraints.application_assignment import ReplicaAssignmentConstraint
from knsp.constraints.node_resource_capacity import NodeResourceCapacityConstraintWithReplicas
from knsp.constraints.node_count import NodeCountConstraintWithReplicas
from knsp.constraints.application_anti_affinity import ReplicaAntiAffinityConstraint
from knsp.objectives.default import DefaultObjective
from knsp.solutions.default import SolutionExtractorWithReplicas

def solve_2_knsp(pd: ProblemData):
    """
    Solves the kubernetes node sizing problem using a minimal set of constraints.
    """
    problem_factory = ProblemFactory(pd)

    # Register default variable definition functions
    problem_factory.register_variables(ApplicationReplicasPlacementVariables())
    problem_factory.register_variables(NodeSelectionVariables())

    # Register default constraint definition functions
    problem_factory.register_constraints(ReplicaAssignmentConstraint())
    problem_factory.register_constraints(NodeResourceCapacityConstraintWithReplicas())
    problem_factory.register_constraints(NodeCountConstraintWithReplicas())
    problem_factory.register_constraints(ReplicaAntiAffinityConstraint())

    # Register the default objective function
    problem_factory.register_objective_function(DefaultObjective())

    # Register the default solution extraction function
    problem_factory.register_solution_extraction_function(SolutionExtractorWithReplicas())

    problem_factory.create_problem()
    return problem_factory.solve()


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

if optimal_cost is not None:
    print(f"Total cost: {optimal_cost}")
    for n in problem_data["node_types"]:
        print(f"Nodes of type {n} used: {node_counts[n]}")
        for i, apps in enumerate(assignment[n]):
            if apps:
                print(f"  Node {i+1}: {', '.join(apps)}")
else:
    print("No feasible solution found.")
