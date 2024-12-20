from ..problem_model import ObjectiveDefinitionInterface

class DefaultObjective(ObjectiveDefinitionInterface):
    def define_objective(self, model, variables, problem_data):
        """Defines the objective function (minimize total cost)."""
        y = variables["y"]
        node_types = problem_data["node_types"]
        cost = problem_data["cost"]
        max_nodes = problem_data["max_nodes"]
        model.Minimize(
            sum(cost[n] * y[n][i] for n in node_types for i in range(max_nodes[n]))
        )
