# Sets

set APPLICATIONS;
set NODE_TYPES;
set RESOURCES;

# Parameters

param r{a in APPLICATIONS, resource in RESOURCES}; # Resource requirement for application 'a'
param c{n in NODE_TYPES, resource in RESOURCES}; # Capacity of resource 'resource' on node 'n'
param cost{n in NODE_TYPES}; # Cost of node 'n'
param replicas{a in APPLICATIONS};

# Parameters for modeling hacks

param max_nodes{n in NODE_TYPES} := # Maximum number of nodes of type 'n'
  max {resource in RESOURCES}
    ceil(sum{a in APPLICATIONS, s in 1..replicas[a]} r[a,resource] / c[n,resource]) + 1;

# Decision Variables

var x{a in APPLICATIONS, s in 1..replicas[a], n in NODE_TYPES, i in 1..max_nodes[n]} binary; # 1 if replica 's' of 'a' is on node 'n', 0 otherwise
var y{n in NODE_TYPES, i in 1..max_nodes[n]} binary; # 1 if node 'i' if type 'n' is used;

# Objective Function

minimize total_cost: sum{n in NODE_TYPES, i in 1..max_nodes[n]} cost[n] * y[n,i];

# Constraints

## 1. Application Assignment: Each application must be assigned to a node

s.t. ApplicationAssignment{a in APPLICATIONS, s in 1..replicas[a]}:
  sum{n in NODE_TYPES, i in 1..max_nodes[n]} x[a,s,n,i] = 1;

## 2. Resource Capacity: Total demand cannot exceed node capacity

s.t. ResourceCapacity{n in NODE_TYPES, i in 1..max_nodes[n], resource in RESOURCES}:
  sum{a in APPLICATIONS, s in 1..replicas[a]} r[a,resource] * x[a,s,n,i] <= c[n,resource] * y[n,i];

## 3. Node Count: Ensure at least one node if any replica is assigned

s.t. NodeCount{a in APPLICATIONS, s in 1..replicas[a], n in NODE_TYPES, i in 1..max_nodes[n]}:
  x[a,s,n,i] <= y[n,i];

## 4. Replica Anti-Affinity: Replicas of the same application on different nodes

s.t. ReplicaAntiAffinity{a in APPLICATIONS, s1 in 1..replicas[a], s2 in 1..replicas[a], n in NODE_TYPES, i in 1..max_nodes[n]: s1 <> s2}:
  x[a,s1,n,i] + x[a,s2,n,i] <= 1;

# Solve the model

solve;

# Postprocessing

## Compute the total number of node of each type
param node_count{n in NODE_TYPES} := sum{i in 1..max_nodes[n]} y[n,i];


# Output the solution

printf "Total cost: %g\n", total_cost;

for {n in NODE_TYPES: node_count[n] > 0} {
    printf "node: %d %s / %d \n", node_count[n], n, max_nodes[n];
    for {i in 1..max_nodes[n]: y[n,i] > 0} {
      printf "%d: ", i;
      for {a in APPLICATIONS, s in 1..replicas[a]: x[a,s,n,i] = 1} {
          printf "%s ", a;
      }
      printf "\n";
    }
    printf "\n";
}

end;
