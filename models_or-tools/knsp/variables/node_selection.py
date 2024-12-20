from ortools.sat.python import cp_model
from typing import Dict, Any, NewType

from .utils import Dimensions, create_nested_variables
from ..problem_model import VariableDefinitionInterface, ProblemData, NodeType, NodeTypes, NodeMax

NodeSelectionVariableType = NewType("NodeSelectionVariableType", Dict[NodeType, Dict[int, cp_model.IntVar]])

NodeSelectionVariableWithTimeIntervalsType = NewType("NodeSelectionVariableWithTimeIntervalsType", Dict[int, Dict[NodeType, Dict[int, cp_model.IntVar]]])

class NodeSelectionVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the node usage variables (y)."""
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        dimensions: Dimensions = [
            node_types,
            lambda parent_keys: range(max_nodes[parent_keys[0]]), # Get max_nodes based on node_type
        ]

        y: NodeSelectionVariableType = create_nested_variables(model, dimensions, "y")

        return {"y": y}

class NodeSelectionVariablesWithTimeIntervals(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the node usage variables (y)."""

        time_intervals: int = problem_data["time_intervals"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        dimensions: Dimensions = [
            range(time_intervals),
            node_types,
            lambda parent_keys: range(max_nodes[parent_keys[1]]), # Get max_nodes based on node_type
        ]

        y: NodeSelectionVariableWithTimeIntervalsType = create_nested_variables(model, dimensions, "y")

        return {"y": y}
