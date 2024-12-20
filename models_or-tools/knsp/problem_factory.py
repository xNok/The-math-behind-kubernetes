import math

from ortools.sat.cp_model_pb2 import CpSolverStatus

from .problem_model import *

class ProblemFactory:
    """
    A factory class to construct the application placement problem.
    """
    def __init__(self, problem_data: ProblemData):
        self.problem_data: ProblemData = problem_data
        self.model: cp_model.CpModel = cp_model.CpModel()
        self.variable_definition_functions: List[VariableDefinitionInterface] = []
        self.constraint_definition_functions: List[ConstraintDefinitionInterface] = []
        self.objective_function: ObjectiveDefinitionInterface | None = None
        self.solution_extraction_function: SolutionExtractionInterface | None = None
        self.variables: Dict[str, Any] = {}

    def register_variables(self, variable_definition: VariableDefinitionInterface) -> None:
        """Registers a variable definition function object."""
        if not isinstance(variable_definition, VariableDefinitionInterface):
            raise TypeError("The provided object must be an instance of VariableDefinitionInterface")
        self.variable_definition_functions.append(variable_definition)

    def register_constraints(self, constraint_definition: ConstraintDefinitionInterface) -> None:
        """Registers a constraint definition function object."""
        if not isinstance(constraint_definition, ConstraintDefinitionInterface):
            raise TypeError("The provided object must be an instance of ConstraintDefinitionInterface")
        self.constraint_definition_functions.append(constraint_definition)

    def register_objective_function(self, objective_definition: ObjectiveDefinitionInterface) -> None:
        """Registers the objective function object."""
        if not isinstance(objective_definition, ObjectiveDefinitionInterface):
            raise TypeError("The provided object must be an instance of ObjectiveDefinitionInterface")
        self.objective_function = objective_definition

    def register_solution_extraction_function(self, solution_extraction: SolutionExtractionInterface) -> None:
        """Registers the solution extraction function object."""
        if not isinstance(solution_extraction, SolutionExtractionInterface):
            raise TypeError("The provided object must be an instance of SolutionExtractionInterface")
        self.solution_extraction_function = solution_extraction

    def create_problem(self) -> cp_model.CpModel:
        """Creates the model, variables, constraints, and objective."""
        self._calculate_max_nodes()
        self._define_variables()
        self._define_constraints()
        self._define_objective()
        return self.model

    def _calculate_max_nodes(self) -> None:
        """Calculates the maximum number of nodes needed for each type."""
        self.problem_data["max_nodes"] = {}

        applications: Applications = self.problem_data["applications"]
        resources: Resources = self.problem_data["resources"]
        r: ResourceRequirements = self.problem_data["r"]
        c: ResourceCapacities = self.problem_data["c"]

        for n in self.problem_data["node_types"]:
            self.problem_data["max_nodes"][n] = max(
                math.ceil(sum(r[a][resource] for a in applications) / c[n][resource])
                for resource in resources
            ) + 1

    def _define_variables(self) -> None:
        """Defines the variables using the registered functions."""
        for func in self.variable_definition_functions:
            self.variables.update(func.define_variables(self.model, self.problem_data))

    def _define_constraints(self) -> None:
        """Defines the constraints using the registered functions."""
        for func in self.constraint_definition_functions:
            func.add_constraint(self.model, self.variables, self.problem_data)

    def _define_objective(self) -> None:
        """Defines the objective function."""
        if self.objective_function:
            self.objective_function.define_objective(self.model, self.variables, self.problem_data)

    def solve(self) -> tuple[float, dict[NodeType, list[list[Application]]], dict[NodeType, int]] | tuple[None, None, None]:
        """Solves the problem created by the factory."""
        solver: cp_model.CpSolver = cp_model.CpSolver()

        self.model.ExportToFile("model.txt")

        status: CpSolverStatus = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            if self.solution_extraction_function:
                optimal_cost, assignment, node_counts = self.solution_extraction_function.extract_solution(
                    solver, self.variables, self.problem_data
                )
                return optimal_cost, assignment, node_counts
            else:
                return None, None, None
        else:
            return None, None, None
