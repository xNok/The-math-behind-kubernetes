import numpy as np
import cpmpy as cp
import math

from ..problem import ProblemData

def max_resource_load(pb: ProblemData, resource: str):
    return sum(pb["applications_requests"][a][resource] for a in pb["application_types"])

def max_nodes(pb: ProblemData, n: str):
    return max(
            math.ceil(max_resource_load(pb, resource) / pb["node_capacity"][n][resource])
            for resource in pb["resource_types"]
        ) + 1

def enumerate_nodes(pb: ProblemData):
    return [n
        for n in pb["node_types"]
        for i in range(max_nodes(pb, n))
    ]

def enumerate_apps(pb: ProblemData):
    return [a
        for a in pb["application_types"]
        for s in range(pb["applications_replicas"][a])
    ]

def solver(pb: ProblemData):

    # Define a set of hypothetical node the load can be assigned to
    nodes = enumerate_nodes(pb)
    apps  = enumerate_apps(pb)

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
    for r in pb["resource_types"]:
        for n, node in enumerate(nodes):
            model += cp.sum(
                    pb["applications_requests"][app][r] * x[a, n] for a, app in apps
                ) <= pb["node_capacity"][node][r] * y[n]

    model.minimize(cp.sum(y))
    solver = cp.SolverLookup.get("ortools", model)

    if solver.solve():
        print("Solution:")
        return model.objective_value()
    else:
        print("No solution found.")
        return 0
    