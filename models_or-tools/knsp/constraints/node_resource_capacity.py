from typing import Dict, Any

from ortools.sat.python import cp_model

from ..problem_model import ConstraintDefinitionInterface, Application, NodeType, Applications, NodeTypes, Resources, ResourceRequirements, ResourceCapacities


class NodeResourceCapacityConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: Dict[str, Any]) -> None:
        """Ensures resource demand does not exceed node capacity."""
        x: Dict[Application, Dict[NodeType, Dict[int, cp_model.IntVar]]] = variables["x"]
        y: Dict[NodeType, Dict[int, cp_model.IntVar]] = variables["y"]
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
