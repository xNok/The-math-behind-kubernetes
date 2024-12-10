# Sets

set APPLICATIONS;
set NODES;
set RESOURCES;
set REPLICAS{a in APPLICATIONS}; 

# Parameters

param r{a in APPLICATIONS, resource in RESOURCES}; # Resource requirement for application 'a'
param c{n in NODES, resource in RESOURCES}; # Capacity of resource 'resource' on node 'n'
param cost{n in NODES}; # Cost of node 'n'

# Parameters for modeling hacks

param max_nodes; # Maximum number of nodes (constant for all types)
param M; # A large constant

# Decision Variables

var x{a in APPLICATIONS, s in REPLICAS[a], n in NODES, i in 1..max_nodes} binary; # 1 if replica 's' of 'a' is on node 'n', 0 otherwise
var y{n in NODES} integer >= 0; # Number of nodes of type 'n'

# Objective Function

minimize total_cost: sum{n in NODES} cost[n] * y[n];

# Constraints

## 1. Application Assignment: Each application must be assigned to a node

s.t. ApplicationAssignment{a in APPLICATIONS, s in REPLICAS[a]}:
  sum{n in NODES, i in 1..max_nodes} x[a,s,n,i] = 1;

## 2. Resource Capacity: Total demand cannot exceed node capacity

s.t. ResourceCapacity{n in NODES, resource in RESOURCES}:
  sum{a in APPLICATIONS, s in REPLICAS[a], i in 1..max_nodes} r[a,resource] * x[a,s,n,i] <= c[n,resource] * y[n];

## 3. Node Count: Ensure at least one node if any replica is assigned

s.t. NodeCount{n in NODES, a in APPLICATIONS,  s in REPLICAS[a]}: 
  sum{i in 1..max_nodes} x[a,s,n,i] <= y[n];

## 4. Replica Anti-Affinity: Replicas of the same application on different nodes

s.t. ReplicaAntiAffinity{a in APPLICATIONS, s1 in REPLICAS[a], s2 in REPLICAS[a], n in NODES, i in 1..max_nodes: s1 <> s2}:
  x[a,s1,n,i] + x[a,s2,n,i] <= 1; 

# Solve the model

solve;

# Output the solution

printf "Total cost: %g\n", total_cost;

for {n in NODES, i in 1..max_nodes: y[n] > 0} {
    for {a in APPLICATIONS, s in REPLICAS[a]: x[a,s,n,i] = 1} {
        printf " Replica %d of application %s on node %s %d\n", s, a, n, i;
    }
}

end;
