from ..problem_model import ConstraintDefinitionInterface

class ApplicationAssignmentConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures each application is assigned to exactly one node."""
        x = variables["x"]
        applications = problem_data["applications"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]
        for a in applications:
            model.AddExactlyOne(x[a][n][i] for n in node_types for i in range(max_nodes[n]))
