from ..problem_model import ConstraintDefinitionInterface, Applications, Replicas, NodeTypes, NodeMax
from ..variables.application_placement import ApplicationReplicasPlacementVariableType, ApplicationPlacementVariableType

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
