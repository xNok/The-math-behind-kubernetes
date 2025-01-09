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
    return [(n,i)
        for n in pb["node_types"]
        for i in range(max_nodes(pb, n))
    ]

def enumerate_apps(pb: ProblemData):
    return [(a,s)
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
    
    