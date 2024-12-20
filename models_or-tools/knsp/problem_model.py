from ortools.sat.python import cp_model
from abc import ABC, abstractmethod
from typing import Dict, List, Any, NewType

# --- Type Aliases ---

# Define Application type
Application = NewType('Application', str)
Applications = NewType('Applications', List[Application])

# Define Resource type
Resource = NewType('Resource', str)

# Define NodeType type
NodeType = NewType('NodeType', str)
NodeTypes = NewType('NodeTypes', List[NodeType])

# Define ResourceRequirements type
ResourceRequirements = NewType('ResourceRequirements', Dict[Application, Dict[Resource, int]])

# Define ResourceCapacities type
ResourceCapacities = NewType('ResourceCapacities', Dict[NodeType, Dict[Resource, int]])

# Define NodeCost type
NodeCost = NewType('NodeCost', Dict[NodeType, int])

# Define MaxNode type
NodeMax = NewType('NodeMax', Dict[NodeType, int])

# ProblemData type
ProblemData = Dict[str, Any]

# --- Interfaces ---

class VariableDefinitionInterface(ABC):
    """Interface for variable definition functions."""
    @abstractmethod
    def define_variables(self, model: cp_model.CpModel, problem_data: ProblemData) -> Dict[str, Any]:
        """
        Defines variables and adds them to the model.

        Args:
            model: The cp_model.CpModel instance.
            problem_data: A dictionary containing problem data.

        Returns:
            A dictionary of the defined variables.
        """
        pass

class ConstraintDefinitionInterface(ABC):
    """Interface for constraint definition functions."""
    @abstractmethod
    def add_constraint(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """
        Adds a constraint to the model.

        Args:
            model: The cp_model.CpModel instance.
            variables: A dictionary of variables defined in the model.
            problem_data: A dictionary containing problem data.
        """
        pass

class ObjectiveDefinitionInterface(ABC):
    """Interface for the objective definition function."""
    @abstractmethod
    def define_objective(self, model: cp_model.CpModel, variables: Dict[str, Any], problem_data: ProblemData) -> None:
        """
        Defines the objective function for the model.

        Args:
            model: The cp_model.CpModel instance.
            variables: A dictionary of variables defined in the model.
            problem_data: A dictionary containing problem data.
        """
        pass

class SolutionExtractionInterface(ABC):
    """Interface for the solution extraction function."""
    @abstractmethod
    def extract_solution(self, solver: cp_model.CpSolver, variables: Dict[str, Any], problem_data: ProblemData) -> tuple[float, dict[NodeType, list[list[Application]]], dict[NodeType, int]]:
        """
        Extracts the solution from the solver.

        Args:
            solver: The cp_model.CpSolver instance.
            variables: A dictionary of variables defined in the model.
            problem_data: A dictionary containing problem data.

        Returns:
            A tuple containing the optimal cost, assignment, and node counts,
            or other relevant solution information.
        """
        pass
