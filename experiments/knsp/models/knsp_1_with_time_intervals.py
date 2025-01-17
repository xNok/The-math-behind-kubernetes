import numpy as np
import cpmpy as cp
import math

from ..problem import ProblemData, ProblemReps
from .knsp_0_initial_model import create_model as create_submodel

def create_model(pb: ProblemReps):
    xs = []
    ys = []
    const = []
    
    for t in range(pb.data["time_intervals"]):
        submodel, x, y = create_submodel(pb, t)
        xs.append(x)
        ys.append(y)
        const += submodel.constraints

    model = cp.Model(const)
    model.minimize(cp.sum(pb.np_nodes_cost_weights() * y for y in ys))

    return model, x, y
    