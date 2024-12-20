from ..problem_model import ConstraintDefinitionInterface, Applications, Replicas, ReplicaWithTime, NodeTypes, NodeMax
from ..variables.application_placement import ApplicationReplicasPlacementVariableType, ApplicationPlacementVariableType, ApplicationReplicasPlacementVariablesWithTimeIntervalsType

class ApplicationAssignmentConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures each application is assigned to exactly one node."""
        x: ApplicationPlacementVariableType = variables["x"]
        applications: Applications = problem_data["applications"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax  = problem_data["max_nodes"]
        for a in applications:
            model.AddExactlyOne(x[a][n][i] for n in node_types for i in range(max_nodes[n]))

class ReplicaAssignmentConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures each application replica is assigned to exactly one node."""
        x: ApplicationReplicasPlacementVariableType = variables["x"]
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax  = problem_data["max_nodes"]
        for a in applications:
            for s in range(replicas[a]):
                model.AddExactlyOne(x[a][s][n][i] for n in node_types for i in range(max_nodes[n]))

class ReplicaAssignmentConstraintWithTimeIntervals(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures each application replica is assigned to exactly one node."""
        x: ApplicationReplicasPlacementVariablesWithTimeIntervalsType = variables["x"]

        time_intervals: int = problem_data["time_intervals"]
        applications: Applications = problem_data["applications"]
        replicas: ReplicaWithTime = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax  = problem_data["max_nodes"]

        for t in range(time_intervals):
            for a in applications:
                for s in range(replicas[a][t]):
                    model.AddExactlyOne(x[t][a][s][n][i] for n in node_types for i in range(max_nodes[n]))
