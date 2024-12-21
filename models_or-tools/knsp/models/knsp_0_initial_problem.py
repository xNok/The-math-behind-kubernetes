from ..problem_factory import ProblemFactory
from ..problem_model import ProblemData
from ..variables.node_selection import NodeSelectionVariables
from ..variables.application_placement import ApplicationPlacementVariables
from ..constraints.application_assignment import ApplicationAssignmentConstraint
from ..constraints.node_resource_capacity import NodeResourceCapacityConstraint
from ..constraints.node_count import NodeCountConstraint
from ..objectives.default import DefaultObjective
from ..solutions.default import DefaultSolutionExtractor
from ..params.max_nodes import MaxNode

def solve_0_knsp(pd: ProblemData):
    """
    Solves the kubernetes node sizing problem using a minimal set of constraints.
    """
    problem_factory = ProblemFactory(pd)

    # Register param resolver function
    problem_factory.register_params(MaxNode())

    # Register default variable definition functions
    problem_factory.register_variables(ApplicationPlacementVariables())
    problem_factory.register_variables(NodeSelectionVariables())

    # Register default constraint definition functions
    problem_factory.register_constraints(ApplicationAssignmentConstraint())
    problem_factory.register_constraints(NodeResourceCapacityConstraint())
    problem_factory.register_constraints(NodeCountConstraint())

    # Register the default objective function
    problem_factory.register_objective_function(DefaultObjective())

    # Register the default solution extraction function
    problem_factory.register_solution_extraction_function(DefaultSolutionExtractor())

    problem_factory.create_problem()
    return problem_factory.solve()

