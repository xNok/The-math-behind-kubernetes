from ortools.sat.python import cp_model
from typing import Dict, Any, NewType

from .utils import Dimensions, create_nested_variables
from ..problem_model import VariableDefinitionInterface, ProblemData, Application, NodeType, Applications, NodeTypes, NodeMax, Replicas, Replica, ReplicasWithTime

# Define ApplicationPlacementVariableType using generics
ApplicationPlacementVariableType = NewType("ApplicationPlacementVariableType",
                                           Dict[Application, Dict[NodeType, Dict[int, cp_model.IntVar]]])

# Define ApplicationReplicasPlacementVariableType using generics
ApplicationReplicasPlacementVariableType = NewType("ApplicationReplicasPlacementVariableType",
                                                   Dict[Application, Dict[Replica, Dict[NodeType, Dict[int, cp_model.IntVar]]]])

# Define ApplicationReplicasPlacementVariablesWithTimeIntervalsType using generics
ApplicationReplicasPlacementVariablesWithTimeIntervalsType = NewType("ApplicationReplicasPlacementVariableType",
                                                                     Dict[int, Dict[Application, Dict[Replica, Dict[NodeType, Dict[int, cp_model.IntVar]]]]])


class ApplicationPlacementVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the application placement variables (x)."""
        applications: Applications = problem_data["applications"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        dimensions: Dimensions = [
            applications,
            node_types,
            lambda parent_keys: range(max_nodes[parent_keys[1]]), # Get max_nodes based on node_type
        ]

        x: ApplicationPlacementVariableType = create_nested_variables(model, dimensions, "x")

        return {"x": x}

class ApplicationReplicasPlacementVariables(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the application replicas placement variables (x)."""
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        dimensions: Dimensions = [
            applications,
            lambda parent_keys: range(replicas[parent_keys[0]]), # Get replicas based on application type
            node_types,
            lambda parent_keys: range(max_nodes[parent_keys[2]]), # Get max_nodes based on node_type
        ]

        x: ApplicationPlacementVariableType = create_nested_variables(model, dimensions, "x")

        return {"x": x}

class ApplicationReplicasPlacementVariablesWithTimeIntervals(VariableDefinitionInterface):
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """Defines the application replicas placement variables (x)."""
        time_intervals: int = problem_data["time_intervals"]
        applications: Applications = problem_data["applications"]
        replicas: ReplicasWithTime = problem_data["replicas"]
        node_types: NodeTypes = problem_data["node_types"]
        max_nodes: NodeMax = problem_data["max_nodes"]

        dimensions: Dimensions = [
            range(time_intervals),
            applications,
            lambda parent_keys: range(replicas[parent_keys[1]][parent_keys[0]]), # Get replicas based on application type
            node_types,
            lambda parent_keys: range(max_nodes[parent_keys[3]]), # Get max_nodes based on node_type
        ]

        x: ApplicationReplicasPlacementVariablesWithTimeIntervalsType = create_nested_variables(model, dimensions, "x")

        return {"x": x}
