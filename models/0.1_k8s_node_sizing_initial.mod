# Sets

set APPLICATIONS;
set RESOURCES;
set NODE_TYPES;

# Parameters

param r{a in APPLICATIONS, resource in RESOURCES}; # Resource requirement for application 'a'
param c{n in NODE_TYPES, resource in RESOURCES}; # Capacity of resource 'resource' on node 'n'
param cost{n in NODE_TYPES}; # Cost of node 'n'

param max_node{n in NODE_TYPES}; # Maximum number of nodes of type 'n'
param M; # A large constant

# Decision Variables

var x{a in APPLICATIONS, n in NODE_TYPES, i in 1..max_node[n]} binary; # 1 if application 'a' is on node 'n', 0 otherwise
var y{n in NODE_TYPES, i in 1..max_node[n]} binary; # 1 if node 'i' if type 'n' is used;

# Objective Function

minimize total_cost: sum{n in NODE_TYPES, i in 1..max_node[n]} cost[n] * y[n,i];

# Constraints

## 1. Application Assignment: Each application must be assigned to a node

s.t. ApplicationAssignment{a in APPLICATIONS}:
  sum{n in NODE_TYPES, i in 1..max_node[n]} x[a,n,i] = 1;

## 2. Resource Capacity: Total demand cannot exceed node capacity

s.t. ResourceCapacity{n in NODE_TYPES, i in 1..max_node[n], resource in RESOURCES}:
  sum{a in APPLICATIONS} r[a,resource] * x[a,n,i] <= c[n,resource] * y[n,i];

## 3. Node Count: Ensure at least one node if any replica is assigned

s.t. NodeCount{a in APPLICATIONS, n in NODE_TYPES, i in 1..max_node[n]}:
  x[a,n,i] <= y[n,i];

# Solve the model

solve;

# Output the solution

printf "Total cost: %g\n", total_cost;

for {n in NODE_TYPES} {
    for {a in APPLICATIONS, i in 1..max_node[n]: x[a,n,i] = 1} {
        printf " application %s on %s %d\n", a,n,i;
    }
}

end;
