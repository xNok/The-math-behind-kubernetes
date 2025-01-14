import numpy as np
import cpmpy as cp
import math

from ..problem import ProblemData, ProblemReps

def solver(pb: ProblemData):
    # Make the proble data immutable, the hash is used for validation and caching
    pb = ProblemReps(pb)

    # Define a set of hypothetical node the load can be assigned to
    nodes = pb.enumerate_nodes()
    apps  = pb.enumerate_apps()

    # Decision variables
    # x[i][j] = 1 if application i is placed on node j, 0 otherwise
    x = cp.boolvar(shape=(len(apps), len(nodes)), name="x")
    # y[j] = 1 if mode j is used, 0 otherwise
    y = cp.boolvar(shape=len(nodes), name="y")

    model = cp.Model()

    # Constraints

    # 1. Application Assignment: Each application must be assigned to a node
    for a, _ in enumerate(apps):
        model += cp.sum(x[a]) == 1

    ## 2. Node Capacity: Total demand cannot exceed node capacity
    for r, _ in enumerate(pb.data["resource_types"]):
        for n, _ in enumerate(nodes):
            model += cp.sum(pb.np_applications_requests_weights(r) * x.transpose()[n]) <= pb.np_node_capacity_weight(r)[n] * y[n]

    ## 3. Node Count: Ensure at least one node if any replica is assigned
    for a, _ in enumerate(apps):
        for n, _ in enumerate(nodes):
            model += x[a][n] <= y[n]

    ## 4. Replica Anti-Affinity: Replicas of the same application on different nodes
    for n, _ in enumerate(nodes):
        lp, hp = 0, 0 # two pointer to window thru application replicas
        for s in pb.data["applications_replicas"]:
            hp += s
            model += sum(x.transpose()[n][lp:hp]) <= 1
            lp += s

    model.minimize(cp.sum(pb.np_nodes_cost_weights() * y))
    solver = cp.SolverLookup.get("ortools", model)

    if solver.solve():
        print("Solution:")
        return model.objective_value(), x.value(), y.value()
    else:
        print("No solution found.")
        return -1
    