from typing import Dict, Any

from ortools.sat.python import cp_model

from knsp.problem_model import ConstraintDefinitionInterface, NodeTypes, NodeMax, ProblemData, Applications, Replicas
from knsp.variables.node_selection import NodeSelectionVariableWithTimeIntervalsType
from knsp.variables.application_placement import ApplicationReplicasPlacementVariablesWithTimeIntervalsType


class PreferSmallNodeIndicesConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """Ensures that for a given node type n if node i is used then i-1 is also used"""
        y: NodeSelectionVariableWithTimeIntervalsType = variables["y"]

        time_intervals: int = problem_data["time_intervals"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        for t in range(time_intervals):
            for n in node_types:
                for i in range(1,max_nodes[n]):
                    model.Add(
                        y[t][n][i] <= y[t][n][i-1]
                    )

class PreferSmallReplicasIndicesConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """Ensures that for a given node type n if node i is used then i-1 is also used"""
        x: ApplicationReplicasPlacementVariablesWithTimeIntervalsType = variables["x"]

        time_intervals: int = problem_data["time_intervals"]
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        for t in range(time_intervals):
            for n in node_types:
                for i in range(1,max_nodes[n]):
                    model.Add(
                        sum(x[t][a][s][n][i] for a in applications for s in range(replicas[a][t]))
                        <= sum(x[t][a][s][n][i-1] for a in applications for s in range(replicas[a][t]))
                    )
