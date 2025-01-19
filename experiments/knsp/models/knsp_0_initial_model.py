import numpy as np
import cpmpy as cp
import math

from ..problem import ProblemReps

# Solve the problem for a given time interval only, by default t=0
def create_model(pb: ProblemReps, t:int = 0):
    # Decision variables
    # x[i][j] = 1 if application i is placed on node j, 0 otherwise
    x = cp.boolvar(shape=(len(pb.apps(t)), len(pb.nodes())), name=f"x({t})")
    # y[j] = 1 if mode j is used, 0 otherwise
    y = cp.boolvar(shape=len(pb.nodes()), name=f"y({t})")

    model = cp.Model()

    # Constraints

    # 1. Application Assignment: Each application must be assigned to a node
    for a, _ in enumerate(pb.apps(t)):
        model += cp.sum(x[a]) == 1

    ## 2. Node Capacity: Total demand cannot exceed node capacity
    for r, _ in enumerate(pb.data["resource_types"]):
        for n, _ in enumerate(pb.nodes()):
            model += cp.sum(pb.np_application_requests_weights(r,t) * x.transpose()[n]) <= pb.np_node_capacity_weight(r)[n] * y[n]

    ## 3. Node Count: Ensure y[n] is one if at least one replicas is assigned
    for a, _ in enumerate(pb.apps(t)):
        model += x[a] <= y

    ## 4. Replicas Anti-Affinity: Replicas of the same application on different nodes
    for n, _ in enumerate(pb.nodes()):
        lp, hp = 0, 0 # two pointer to window thru application replicas
        for s in pb.data["application_replicas"][0]:
            hp += s
            model += sum(x.transpose()[n][lp:hp]) <= max(1, s * pb.data["disruption_budget"])
            lp += s

    #### Symmetry breaking

    ## 1. Ensure that node if instance i is used than i-1 is also used
    for n, _ in enumerate(pb.data["node_types"]):
        for i in range(1,pb.max_nodes(n)):
            model += y[i] <= y[i-1]

    model.minimize(cp.sum(pb.np_nodes_cost_weights() * y))
    
    return model, x, y
    