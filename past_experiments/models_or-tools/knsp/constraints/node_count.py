from ..problem_model import ConstraintDefinitionInterface, Replicas
from ..variables.application_placement import ApplicationReplicasPlacementVariableType, ApplicationPlacementVariableType
from ..variables.node_selection import NodeSelectionVariableType


class NodeCountConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures a node is used if an application is assigned to it."""
        x: ApplicationPlacementVariableType = variables["x"]
        y: NodeSelectionVariableType = variables["y"]
        applications = problem_data["applications"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]
        for a in applications:
            for n in node_types:
                for i in range(max_nodes[n]):
                    model.Add(x[a][n][i] <= y[n][i])

class NodeCountConstraintWithReplicas(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures a node is used if an application replicas is assigned to it."""
        x: ApplicationReplicasPlacementVariableType = variables["x"]
        y: NodeSelectionVariableType = variables["y"]
        applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]
        for a in applications:
            for s in range(replicas[a]):
                for n in node_types:
                    for i in range(max_nodes[n]):
                        model.Add(x[a][s][n][i] <= y[n][i])

class NodeCountConstraintWithReplicasWithTimeIntervals(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures a node is used if an application replicas is assigned to it."""
        x: ApplicationReplicasPlacementVariableType = variables["x"]
        y: NodeSelectionVariableType = variables["y"]

        time_intervals: int = problem_data["time_intervals"]
        applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]

        for t in range(time_intervals):
            for a in applications:
                for s in range(replicas[a][t]):
                    for n in node_types:
                        for i in range(max_nodes[n]):
                            model.Add(x[t][a][s][n][i] <= y[t][n][i])
