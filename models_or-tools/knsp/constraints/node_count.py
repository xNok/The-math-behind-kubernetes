from ..problem_model import ConstraintDefinitionInterface

class NodeCountConstraint(ConstraintDefinitionInterface):
    def add_constraint(self, model, variables, problem_data):
        """Ensures a node is used if an application is assigned to it."""
        x = variables["x"]
        y = variables["y"]
        applications = problem_data["applications"]
        node_types = problem_data["node_types"]
        max_nodes = problem_data["max_nodes"]
        for n in node_types:
            for i in range(max_nodes[n]):
                model.Add(sum(x[a][n][i] for a in applications) <= len(applications) * y[n][i])
