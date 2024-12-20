from knsp.problem_factory import ProblemFactory
from knsp.problem_model import ProblemData
from knsp.variables import ApplicationPlacementVariables, NodeSelectionVariables
from knsp.constraints import ApplicationAssignmentConstraint
from knsp.objectives.default import DefaultObjective
from knsp.solutions.default import DefaultSolutionExtractor

def solve_knsp(pd: ProblemData):
    """
    Solves the kubernetes node sizing problem using a minimal set of constraints.
    """
    problem_factory = ProblemFactory(pd)

    # Register default variable definition functions
    problem_factory.register_variables(ApplicationPlacementVariables())
    problem_factory.register_variables(NodeSelectionVariables())

    # Register default constraint definition functions
    problem_factory.register_constraints(ApplicationAssignmentConstraint())
    # problem_factory.register_constraints(add_resource_capacity_constraint)
    # problem_factory.register_constraints(add_node_count_constraint)

    # Register the default objective function
    problem_factory.register_objective_function(DefaultObjective())

    # Register the default solution extraction function
    problem_factory.register_solution_extraction_function(DefaultSolutionExtractor())

    problem_factory.create_problem()
    return problem_factory.solve()


# Example Usage (using data from the MathProg model)
problem_data = {
    "applications": ["A1", "A2", "A3"],
    "resources": ["CPU", "RAM"],
    "node_types": ["N1", "N2"],
    "r": {
        "A1": {"CPU": 2, "RAM": 4},
        "A2": {"CPU": 3, "RAM": 2},
        "A3": {"CPU": 1, "RAM": 3},
    },
    "c": {
        "N1": {"CPU": 4, "RAM": 8},
        "N2": {"CPU": 8, "RAM": 16},
    },
    "cost": {"N1": 10, "N2": 19},
}

optimal_cost, assignment, node_counts = solve_knsp(problem_data)

if optimal_cost is not None:
    print(f"Total cost: {optimal_cost}")
    for n in problem_data["node_types"]:
        print(f"Nodes of type {n} used: {node_counts[n]}")
        for i, apps in enumerate(assignment[n]):
            if apps:
                print(f"  Node {i+1}: {', '.join(apps)}")
else:
    print("No feasible solution found.")
