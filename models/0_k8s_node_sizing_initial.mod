# Sets

set APPLICATIONS;
set NODES;
set RESOURCES;

# Parameters

param r{a in APPLICATIONS, resource in RESOURCES}; # Resource requirement for application 'a'
param c{n in NODES, resource in RESOURCES}; # Capacity of resource 'resource' on node 'n'
param cost{n in NODES}; # Cost of node 'n'
param M; # A large constant

# Decision Variables

var x{a in APPLICATIONS, n in NODES} binary; # 1 if application 'a' is on node 'n', 0 otherwise
var y{n in NODES} integer >= 0; # Number of nodes of type 'n'

# Objective Function

minimize total_cost: sum{n in NODES} cost[n] * y[n];

# Constraints

## 1. Application Assignment: Each application must be assigned to a node

s.t. ApplicationAssignment{a in APPLICATIONS}:
  sum{n in NODES} x[a,n] = 1;

## 2. Resource Capacity: Total demand cannot exceed node capacity

s.t. ResourceCapacity{n in NODES, resource in RESOURCES}:
  sum{a in APPLICATIONS} r[a,resource] * x[a,n] <= c[n,resource] * y[n];

## 3. Node Count: Ensure at least one node if any replica is assigned

s.t. NodeCount{a in APPLICATIONS, n in NODES}:
  x[a,n] <= y[n];

# Solve the model

solve;

# Output the solution

printf "Total cost: %g\n", total_cost;

for {n in NODES: y[n] > 0} {
    printf "Node type %s: %d nodes\n", n, y[n];
    for {a in APPLICATIONS: x[a,n] = 1} {
        printf " application %s\n", a;
    }
}

end;
