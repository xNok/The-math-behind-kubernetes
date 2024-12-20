from ortools.sat.python import cp_model
from typing import Dict, Any

from ..problem_model import VariableDefinitionInterface, ProblemData, Application, NodeType, Applications, NodeTypes, NodeMax


class ApplicationPlacementVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the application placement variables (x)."""
        x: Dict[Application, Dict[NodeType, Dict[int, cp_model.IntVar]]] = {}
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
