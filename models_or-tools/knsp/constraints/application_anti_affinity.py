from ..problem_model import ConstraintDefinitionInterface, Applications, Replicas, NodeTypes, NodeMax
from ..variables.application_placement import ApplicationReplicasPlacementVariableType

class ReplicaAntiAffinityConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures each application is assigned to exactly one node."""
        x: ApplicationReplicasPlacementVariableType = variables["x"]
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax  = problem_data["max_nodes"]
        for a in applications:
            for s1 in range(replicas[a]):
                for s2 in range(replicas[a]):
                    if s1 != s2:
                        for n in node_types:
                            for i in range(max_nodes[n]):
                                model.Add( x[a][s1][n][i] + x[a][s2][n][i] <= 1 )
