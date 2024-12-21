from ..problem_factory import ProblemFactory
from ..problem_model import ProblemData
from ..variables.application_placement import ApplicationReplicasPlacementVariables
from ..variables.node_selection import NodeSelectionVariables
from ..constraints.application_assignment import ReplicaAssignmentConstraint
from ..constraints.node_resource_capacity import NodeResourceCapacityConstraintWithReplicas
from ..constraints.node_count import NodeCountConstraintWithReplicas
from ..constraints.application_anti_affinity import ReplicaAntiAffinityConstraint
from ..objectives.default import DefaultObjective
from ..solutions.default import SolutionExtractorWithReplicas
from ..params.max_nodes import MaxNodeWithReplicas

def solve_1_knsp(pd: ProblemData):
    """
    Solves the kubernetes node sizing problem using a minimal set of constraints.
    """
    problem_factory = ProblemFactory(pd)

    # Register param resolver function
    problem_factory.register_params(MaxNodeWithReplicas())

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
