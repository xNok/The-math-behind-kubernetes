import numpy as np
import cpmpy as cp
import math

from ..problem import ProblemData, ProblemReps

def solver(pb: ProblemData):
    # Make the problem data immutable, the hash is used for validation and caching
    pb = ProblemReps(pb)

    # Decision variables
    # x[t][i][j] = 1 if application i is placed on node j at time t, 0 otherwise
    x = cp.boolvar(shape=(len(pb.data["time_intervals"]), len(pb.apps()), len(pb.nodes())), name="x")
    # y[t][j] = 1 if mode j is used at time t, 0 otherwise
    y = cp.boolvar(shape=(len(pb.data["time_intervals"]),pb.nodes()), name="y")

    model = cp.Model()

    # Constraints

    # 1. Application Assignment: Each application must be assigned to a node
    for t in range(pb.data["time_intervals"]):
        for a, _ in enumerate(pb.apps()):
            model += cp.sum(x[t][a]) == 1

    ## 2. Node Capacity: Total demand cannot exceed node capacity
    for t in range(pb.data["time_intervals"]):
        for r, _ in enumerate(pb.data["resource_types"]):
            for n, _ in enumerate(pb.nodes()):
                model += cp.sum(pb.np_application_requests_weights(r) * x[t].transpose()[n]) <= pb.np_node_capacity_weight(r)[n] * y[t][n]

    ## 3. Node Count: Ensure y[n] is one if at least one replicas is assigned
    for t in range(pb.data["time_intervals"]):
        for a, _ in enumerate(pb.apps()):
            model += x[t][a] <= y[t]

    ## 4. Replicas Anti-Affinity: Replicas of the same application on different nodes
    for t in range(pb.data["time_intervals"]):
        for n, _ in enumerate(pb.nodes()):
            lp, hp = 0, 0 # two pointer to window thru application replicas
            for s in pb.data["application_replicas"][t]:
                hp += s
                model += sum(x.transpose()[n][lp:hp]) <= max(1, s * pb.data["disruption_budget"])
                lp += s

    model.minimize(cp.sum(pb.np_nodes_cost_weights() * y[t] for t in range(pb.data["time_intervals"])))
    solver = cp.SolverLookup.get("ortools", model)

    if solver.solve():
        print("Solution:")
        return model.objective_value(), x.value(), y.value()
    else:
        print("No solution found.")
        return -1
    