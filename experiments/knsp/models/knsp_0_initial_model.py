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
        model += cp.sum(x[a, n] for n, _ in enumerate(nodes)) == 1

    ## 2. Node Capacity: Total demand cannot exceed node capacity
    for r, _ in enumerate(pb.data["resource_types"]):
        for n in nodes:
            model += cp.sum(pb.np_applications_requests_weights(r) * x.transpose()[n]) <= pb.data["node_capacity"][n][r] * y[n]

    model.minimize(cp.sum(y))
    solver = cp.SolverLookup.get("ortools", model)

    if solver.solve():
        print("Solution:")
        return model.objective_value()
    else:
        print("No solution found.")
        return 0
    