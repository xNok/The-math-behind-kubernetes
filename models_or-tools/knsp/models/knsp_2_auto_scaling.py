from ..problem_factory import ProblemFactory
from ..problem_model import ProblemData
from ..variables.application_placement import ApplicationReplicasPlacementVariablesWithTimeIntervals
from ..variables.node_selection import NodeSelectionVariablesWithTimeIntervals
from ..constraints.application_assignment import ReplicaAssignmentConstraintWithTimeIntervals
from ..constraints.node_resource_capacity import NodeResourceCapacityConstraintWithReplicasWithTimeIntervals
from ..constraints.node_count import NodeCountConstraintWithReplicasWithTimeIntervals
from ..constraints.application_anti_affinity import ReplicaAntiAffinityConstraintWithTimeIntervals
from ..constraints.application_anti_descheduling import ReplicasAntiDeschedulingVariables
from ..objectives.default import TimeBaseObjective
from ..solutions.timebased import SolutionExtractorWithReplicasWithTimeIntervals
from ..params.max_nodes import MaxNodeWithReplicasWithTimeIntervals

def solve_2_knsp(pd: ProblemData):
    """
    Solves the kubernetes node sizing problem using a minimal set of constraints.
    """
    problem_factory = ProblemFactory(pd)

    # Register param resolver function
    problem_factory.register_params(MaxNodeWithReplicasWithTimeIntervals())

    # Register default variable definition functions
    problem_factory.register_variables(ApplicationReplicasPlacementVariablesWithTimeIntervals())
    problem_factory.register_variables(NodeSelectionVariablesWithTimeIntervals())

    # Register default constraint definition functions
    problem_factory.register_constraints(ReplicaAssignmentConstraintWithTimeIntervals())
    problem_factory.register_constraints(NodeResourceCapacityConstraintWithReplicasWithTimeIntervals())
    problem_factory.register_constraints(NodeCountConstraintWithReplicasWithTimeIntervals())
    problem_factory.register_constraints(ReplicaAntiAffinityConstraintWithTimeIntervals())
    problem_factory.register_constraints(ReplicasAntiDeschedulingVariables())

    # Register the default objective function
    problem_factory.register_objective_function(TimeBaseObjective())

    # Register the default solution extraction function
    problem_factory.register_solution_extraction_function(SolutionExtractorWithReplicasWithTimeIntervals())

    problem_factory.create_problem()
    return problem_factory.solve()

