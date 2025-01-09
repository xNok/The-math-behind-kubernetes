from ..problem_model import ConstraintDefinitionInterface, Applications, Replicas, NodeTypes, NodeMax
from ..variables.application_placement import ApplicationReplicasPlacementVariablesWithTimeIntervalsType


class ReplicasAntiDeschedulingVariables(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures each application is assigned to exactly one node."""
        x: ApplicationReplicasPlacementVariablesWithTimeIntervalsType = variables["x"]

        time_intervals: int = problem_data["time_intervals"]
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax  = problem_data["max_nodes"]

        for t1 in range(time_intervals):
            for t2 in range(time_intervals):
                if t1 - t2 == 1:
                    for a in applications:
                        for s in range(min(replicas[a][t1], replicas[a][t2])):
                            for n in node_types:
                                for i in range(max_nodes[n]):
                                    model.Add(x[t1][a][s][n][i] <= x[t2][a][s][n][i])
