from typing import Dict, Any

from ortools.sat.python import cp_model

from knsp.problem_model import ConstraintDefinitionInterface, NodeTypes, NodeMax, ProblemData
from knsp.variables.node_selection import NodeSelectionVariableWithTimeIntervalsType

class MaxNodeTypeCountConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """Ensures that for a given node type n if node i is used then i-1 is also used"""
        y: NodeSelectionVariableWithTimeIntervalsType = variables["y"]

        time_intervals: int = problem_data["time_intervals"]
        node_types: NodeTypes = problem_data["node_types"]
        max_node_types: int = problem_data["max_node_type"] if "max_node_type" in problem_data else len(node_types)

        for t in range(time_intervals):
            model.Add(
                sum(y[t][n][0] for n in node_types) <= max_node_types
            )
