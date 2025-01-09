import math

from ..problem_model import ParamDefinitionInterface, Applications, Resources, ResourceRequirements, ResourceCapacities, ProblemData, Replicas


class MaxNode(ParamDefinitionInterface):
    def add_param(self, problem_data: ProblemData) -> ProblemData:
        """Calculates the maximum number of nodes needed for each type."""
        problem_data["max_nodes"] = {}

        applications: Applications = problem_data["applications"]
        resources: Resources = problem_data["resources"]
        r: ResourceRequirements = problem_data["r"]
        c: ResourceCapacities = problem_data["c"]

        for n in problem_data["node_types"]:
            problem_data["max_nodes"][n] = max(
                math.ceil(sum(r[a][resource] for a in applications) / c[n][resource])
                for resource in resources
            ) + 1

        return problem_data

class MaxNodeWithReplicas(ParamDefinitionInterface):
    def add_param(self, problem_data: ProblemData) -> ProblemData:
        """Calculates the maximum number of nodes needed for each type."""
        problem_data["max_nodes"] = {}

        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        resources: Resources = problem_data["resources"]
        r: ResourceRequirements = problem_data["r"]
        c: ResourceCapacities = problem_data["c"]

        for n in problem_data["node_types"]:
            problem_data["max_nodes"][n] = max(
                math.ceil(sum(r[a][resource] for a in applications for _ in range(replicas[a])) / c[n][resource])
                for resource in resources
            ) + 1

        return problem_data

class MaxNodeWithReplicasWithTimeIntervals(ParamDefinitionInterface):
    def add_param(self, problem_data: ProblemData) -> ProblemData:
        """Calculates the maximum number of nodes needed for each type."""
        problem_data["max_nodes"] = {}

        time_intervals: int = problem_data["time_intervals"]
        applications: Applications = problem_data["applications"]
        replicas: Replicas = problem_data["replicas"]
        resources: Resources = problem_data["resources"]
        r: ResourceRequirements = problem_data["r"]
        c: ResourceCapacities = problem_data["c"]

        for n in problem_data["node_types"]:
            problem_data["max_nodes"][n] = max(
                math.ceil(sum(r[a][resource] for a in applications for _ in range(replicas[a][t])) / c[n][resource])
                for resource in resources for t in range(time_intervals)
            ) + 1

        return problem_data
