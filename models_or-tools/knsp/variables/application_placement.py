from ortools.sat.python import cp_model
from typing import Dict, Any, NewType

from ..problem_model import VariableDefinitionInterface, ProblemData, Application, NodeType, Applications, NodeTypes, NodeMax, Replicas, Replica

ApplicationPlacementVariableType = NewType("ApplicationPlacementVariableType", Dict[Application, Dict[NodeType, Dict[int, cp_model.IntVar]]])

class ApplicationPlacementVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the application placement variables (x)."""
        x: ApplicationPlacementVariableType = {}
        applications: Applications = problem_data["applications"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]
        for a in applications:
            x[a] = {}
            for n in node_types:
                x[a][n] = {}
                for i in range(max_nodes[n]):
                    x[a][n][i] = model.NewBoolVar(f'x[{a}][{n}][{i}]')
        return {"x": x}

ApplicationReplicasPlacementVariableType = NewType("ApplicationReplicasPlacementVariableType", Dict[Application, Dict[int, Dict[NodeType, Dict[int, cp_model.IntVar]]]])

class ApplicationReplicasPlacementVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the application replicas placement variables (x)."""
        x: ApplicationReplicasPlacementVariableType = {}
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]
        for a in applications:
            x[a] = {}
            for s in range(replicas[a]):
                x[a][s] = {}
                for n in node_types:
                    x[a][s][n] = {}
                    for i in range(max_nodes[n]):
                        x[a][s][n][i] = model.NewBoolVar(f'x[{a}][{s}][{n}][{i}]')
        return {"x": x}
