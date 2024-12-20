from ortools.sat.python import cp_model
from typing import Dict, Any, NewType

from ..problem_model import VariableDefinitionInterface, ProblemData, NodeType, NodeTypes, NodeMax

NodeSelectionVariableType = NewType("NodeSelectionVariableType", Dict[NodeType, Dict[int, cp_model.IntVar]])

class NodeSelectionVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the node usage variables (y)."""
        y: NodeSelectionVariableType = {}
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]
        for n in node_types:
            y[n] = {}
            for i in range(max_nodes[n]):
                y[n][i] = model.NewBoolVar(f'y[{n}][{i}]')
        return {"y": y}
