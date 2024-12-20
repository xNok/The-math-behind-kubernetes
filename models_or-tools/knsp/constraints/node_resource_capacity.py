from typing import Dict, Any

from ortools.sat.python import cp_model

from ..problem_model import ConstraintDefinitionInterface, Application, NodeType, Applications, NodeTypes, Resources, ResourceRequirements, ResourceCapacities, ProblemData, Replicas
from ..variables.application_placement import ApplicationPlacementVariableType, ApplicationReplicasPlacementVariableType
from ..variables.node_selection import NodeSelectionVariableType

class NodeResourceCapacityConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """Ensures resource demand does not exceed node capacity."""
        x: ApplicationPlacementVariableType = variables["x"]
        y: NodeSelectionVariableType = variables["y"]

        applications: Applications = problem_data["applications"]
        node_types: NodeTypes = problem_data["node_types"]
        resources: Resources = problem_data["resources"]
        r: ResourceRequirements = problem_data["r"]
        c: ResourceCapacities = problem_data["c"]
        max_nodes: Dict[NodeType, int] = problem_data["max_nodes"]
        for n in node_types:
            for i in range(max_nodes[n]):
                for resource in resources:
                    model.Add(
                        sum(r[a][resource] * x[a][n][i] for a in applications)
                        <= c[n][resource] * y[n][i]
                    )

class NodeResourceCapacityConstraintWithReplicas(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """Ensures resource demand does not exceed node capacity."""
        x: ApplicationReplicasPlacementVariableType = variables["x"]
        y: NodeSelectionVariableType = variables["y"]

        # dimensions
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        resources: Resources = problem_data["resources"]
        max_nodes: Dict[NodeType, int] = problem_data["max_nodes"]

        # coefficients
        r: ResourceRequirements = problem_data["r"]
        c: ResourceCapacities = problem_data["c"]

        for n in node_types:
            for i in range(max_nodes[n]):
                for resource in resources:
                    model.Add(
                        sum(r[a][resource] * x[a][s][n][i] for a in applications for s in range(replicas[a]))
                        <= c[n][resource] * y[n][i]
                    )

class NodeResourceCapacityConstraintWithReplicasWithTimeIntervals(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """Ensures resource demand does not exceed node capacity."""
        x: ApplicationReplicasPlacementVariableType = variables["x"]
        y: NodeSelectionVariableType = variables["y"]

        # dimensions
        time_intervals: int = problem_data["time_intervals"]
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        resources: Resources = problem_data["resources"]
        max_nodes: Dict[NodeType, int] = problem_data["max_nodes"]

        # coefficient
        r: ResourceRequirements = problem_data["r"]
        c: ResourceCapacities = problem_data["c"]

        for t in range(time_intervals):
            for n in node_types:
                for i in range(max_nodes[n]):
                    for resource in resources:
                        model.Add(
                            sum(r[a][resource] * x[t][a][s][n][i] for a in applications for s in range(replicas[a][t]))
                            <= c[n][resource] * y[t][n][i]
                        )
