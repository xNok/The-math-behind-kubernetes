# Sets

set APPLICATIONS;
set NODE_TYPES;
set RESOURCES;
set TIME_INTERVALS;

# Parameters

param r{a in APPLICATIONS, resource in RESOURCES}; # Resource requirement for application 'a'
param c{n in NODE_TYPES, resource in RESOURCES}; # Capacity of resource 'resource' on node 'n'
param cost{n in NODE_TYPES}; # Cost of node 'n'
param replicas{a in APPLICATIONS, t in TIME_INTERVALS}; # Number of replicas for application 'a' at time 't'

# Parameters for modeling hacks

param max_nodes_overflow := 2;

param max_nodes{n in NODE_TYPES} := # Maximum number of nodes of type 'n'
  max {resource in RESOURCES, t in TIME_INTERVALS}
    ceil(sum{a in APPLICATIONS, s in 1..replicas[a,t]} r[a,resource] / c[n,resource]) * max_nodes_overflow;

param max_node_types;  # Maximum number of node types allowed

# Sets for modeling convenience

set NODE_INSTANCES := setof{n in NODE_TYPES, i in 1..max_nodes[n]} (n,i);
set APPLICATION_REPLICAS{t in TIME_INTERVALS} := setof{a in APPLICATIONS, s in 1..replicas[a,t]} (a,s);

# Decision Variables

var x{t in TIME_INTERVALS, (a,s) in APPLICATION_REPLICAS[t], (n,i) in NODE_INSTANCES} binary; # 1 if replica 's' of 'a' is on node 'n', 0 otherwise
var y{t in TIME_INTERVALS, (n,i) in NODE_INSTANCES} binary; # 1 if node 'i' if type 'n' is used;

# Objective Function

minimize total_cost: sum{t in TIME_INTERVALS, (n,i) in NODE_INSTANCES} cost[n] * y[t,n,i];

# Constraints

## 1. Application Assignment: Each application must be assigned to a node

s.t. ApplicationAssignment{t in TIME_INTERVALS, (a,s) in APPLICATION_REPLICAS[t]}:
  sum{(n,i) in NODE_INSTANCES} x[t,a,s,n,i] = 1;

## 2. Resource Capacity: Total demand cannot exceed node capacity

s.t. ResourceCapacity{t in TIME_INTERVALS, (n,i) in NODE_INSTANCES, resource in RESOURCES}:
  sum{(a,s) in APPLICATION_REPLICAS[t]} r[a,resource] * x[t,a,s,n,i] <= c[n,resource] * y[t,n,i];

## 3. Node Count: Ensure at least one node if any replica is assigned

s.t. NodeCount{t in TIME_INTERVALS, (a,s) in APPLICATION_REPLICAS[t], (n,i) in NODE_INSTANCES}:
  x[t,a,s,n,i] <= y[t,n,i];

## 4. Replica Anti-Affinity: Replicas of the same application on different nodes

s.t. ReplicaAntiAffinity{t in TIME_INTERVALS, a in APPLICATIONS, s1 in 1..replicas[a,t], s2 in 1..replicas[a,t], (n,i) in NODE_INSTANCES: s1 <> s2}:
  x[t,a,s1,n,i] + x[t,a,s2,n,i] <= 1;

## 5. Replica Anti-Descheduling: Replicas between subsequent time interval can't be reschedule on different node

s.t. AntiDescheduling{t1 in TIME_INTERVALS, t2 in TIME_INTERVALS, a in APPLICATIONS, s in 1..min(replicas[a,t1], replicas[a,t2]), (n,i) in NODE_INSTANCES: t1 - t2 = 1}:
  x[t1,a,s,n,i] <= x[t2,a,s,n,i];

# Symmetry Breaking Constraints:

## 1. Ensure that node instance i is used than i-1 is also used

s.t. PreferSmallNodeIndices{t in TIME_INTERVALS, (n,i) in NODE_INSTANCES: i > 1}:
  y[t,n,i] <= y[t,n,i-1];

## 2. Ensure that replicas s is assigned to node i there is as least a replicas assigne to a node i-1

s.t. PreferSmallReplicasIndices{t in TIME_INTERVALS, (n,i) in NODE_INSTANCES, (a,s) in APPLICATION_REPLICAS[t] : i > 1 and s > 1}:
  x[t,a,s,n,i] <= sum{(a,s2) in APPLICATION_REPLICAS[t]} x[t,a,s2,n,i-1];

## 3. Ensure that node instances with smaller indices are contain the most applications

s.t. PreferMoreApplications{t in TIME_INTERVALS, (n,i) in NODE_INSTANCES: i > 1}:
  sum{(a,s) in APPLICATION_REPLICAS[t]} x[t,a,s,n,i] <= sum{(a,s) in APPLICATION_REPLICAS[t]} x[t,a,s,n,i-1];

## 4. Resource Capacity: Total demand cannot exceed node total capacity (Lazy constaint)

s.t. ResourceTotalCapacity{t in TIME_INTERVALS, resource in RESOURCES}:
  sum{(a,s) in APPLICATION_REPLICAS[t], (n,i) in NODE_INSTANCES} r[a,resource] * x[t,a,s,n,i] <= sum{(n,i) in NODE_INSTANCES} c[n,resource] * y[t,n,i];

# Problem reduction constrains

s.t. MaxNodeTypeCount{t in TIME_INTERVALS}:
  sum{n in NODE_TYPES} y[t,n,1] <= max_node_types;

# Solve the model

solve;

# Postprocessing

## Compute the total number of node of each type

param node_count{t in TIME_INTERVALS, n in NODE_TYPES} := sum{i in 1..max_nodes[n]} y[t,n,i];

# Output the solution

printf "Total cost: %g\n", total_cost;

for {t in TIME_INTERVALS} {
    printf "------- t: %d ------- \n", t;
    for {n in NODE_TYPES: node_count[t,n] > 0} {
      printf " -> %d %s / %d \n", node_count[t,n], n, max_nodes[n];
      for {i in 1..max_nodes[n]: y[t,n,i] > 0} {
        printf "%d: ", i;
        for {(a,s) in APPLICATION_REPLICAS[t]: x[t,a,s,n,i] = 1} {
          printf "%s(%d) ", a,s;
        }
        printf "\n";
      }
    }
    printf "\n";
}

end;
