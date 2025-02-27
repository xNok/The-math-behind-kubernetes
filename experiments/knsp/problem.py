from typing import TypedDict, Tuple, List
from collections import namedtuple
from functools import lru_cache
from immutabledict import immutabledict
import math
import numpy as np

# ProblemData allows to validate the types in the provided dict
class ProblemData(TypedDict):
    # Problem descrition
    # The resources we are optimizing for (eg. CPU, Memory)
    resource_types: Tuple[str]
    # The set of VM type available
    node_types: Tuple[str]
    # List of application that need to be allocated to the cluster
    application_types: Tuple[str]
    # Number of time intervals
    time_intervals: int

    # Numerical values
    # The hourly cost of a node type
    node_cost: Tuple[int]
    # The resource capacity provided for a given node type
    node_capacity: Tuple[int, ...]
    # Resource reserved by a given application
    application_requests: Tuple[int, ...]
    # Number of replicas for a given application for a given time interval
    application_replicas: Tuple[Tuple[int]]

    # % of replicas that can be unavailable
    # 100% -> they can be on same node
    # 0% => they all are on different nodes
    disruption_budget: int

# ProblemReps provide an immutable representation of the problem 
# also provide utility function to easily create constraints, notably numpy array operations
class ProblemReps:

    data: ProblemData

    def __init__(self, pb: ProblemData):
        self.data = immutabledict(pb)

    @lru_cache
    def nodes(self):
        return [n
            for n, _ in enumerate(self.data["node_types"])
            for i in range(self.max_nodes(n))
        ]

    @lru_cache
    def apps(self, t):
        return [a
            for a, _ in enumerate(self.data["application_types"])
            for s in range(self.data["application_replicas"][t][a])
        ]

    # Numpy array access
    @lru_cache
    def node_cost(self):
        return np.array(self.data["node_cost"])

    # Transformation 
    @lru_cache
    def max_resource_load(self, r: int):
        return sum(self.data["application_requests"][a][r] for a, _ in enumerate(self.data["application_types"]))

    @lru_cache
    def max_nodes(self, n: int):
        return max(
                math.ceil(self.max_resource_load(r) / self.data["node_capacity"][n][r])
                for r, _ in enumerate(self.data["resource_types"])
            ) + 1
    
    # Return the weight for application resource
    @lru_cache
    def np_application_requests_weights(self, r: int, t: int):
        return np.array([
            self.data["application_requests"][atype][r]
            for _, atype in enumerate(self.apps(t))
        ])

    @lru_cache
    def np_node_capacity_weight(self, r: int):
        return np.array([
            self.data["node_capacity"][nType][r]
            for _, nType in enumerate(self.nodes())
        ])

    @lru_cache
    def np_nodes_cost_weights(self):
        return np.array([
            self.data["node_cost"][ntype]
            for _, ntype in enumerate(self.nodes())
        ])