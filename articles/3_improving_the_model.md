# The Math behind Kubernetes - Part 3 - Improving the model

The model we have derived and sove in the first two issues is extreamely simple and solutions can be considered as trivial. Given that the cost of a node is invesly proportianal to it's size the optional solution will always be a matter of selecting the large node that accomodate for your worklead. While this is trivial, to my dismay this is the best some application like Kubecost are able to offer. So lets keep modeling and move past this simplistic model to a more realistic one that takes into account the tradeoff associated with managing Kubernetes workload.

The obvious reason to have more that one node is to ensure reliability, if that node where to fail then the entire workload would be at risk. To solve this problem each application is deployed with as a set of replicates. Let's introduce replicated to our model and assume that to ensure reliability replicated of an application can't be scheduled on the same node.

## Defining the KNSP with replicates anti-affinity

In terms of modeling this problem is much more intresting and has some typical modeling challemges

```diff
# Sets

set APPLICATIONS;
set NODES;
set RESOURCES;
+ set REPLICAS{a in APPLICATIONS}; 
```

```diff
# Parameters for modeling hacks

+ param max_nodes; # Maximum number of nodes (constant for all types)
param M; # A large constant
```

```diff
# Decision Variables

- var x{a in APPLICATIONS, n in NODES} binary; # 1 if application 'a' is on node 'n', 0 otherwise
+ var x{a in APPLICATIONS, s in REPLICAS[a], n in NODES, i in 1..max_nodes} binary; # 1 if replica 's' of 'a' is on node 'n', 0 otherwise
var y{n in NODES} integer >= 0; # Number of nodes of type 'n'
```

```diff
## 1. Application Assignment: Each application must be assigned to a node

- s.t. ApplicationAssignment{a in APPLICATIONS}:
-  sum{n in NODES} x[a,n] = 1;
+ s.t. ApplicationAssignment{a in APPLICATIONS, s in REPLICAS[a]}:
+  sum{n in NODES} x[a,s,n] = 1;
```

```diff
## 2. Resource Capacity: Total demand cannot exceed node capacity

s.t. ResourceCapacity{n in NODES, resource in RESOURCES}:
-  sum{a in APPLICATIONS} r[a,resource] * x[a,n] <= c[n,resource] * y[n];
+  sum{a in APPLICATIONS, s in REPLICAS[a]} r[a,resource] * x[a,s,n] <= c[n,resource] * y[n];

```

```diff
## 3. Node Count: Ensure at least one node if any replica is assigned

- s.t. NodeCount{a in APPLICATIONS, n in NODES}:
-  x[a,n] <= y[n];
+ s.t. NodeCount{a in APPLICATIONS, s in REPLICAS[a], n in NODES}:
+  x[a,s,n] <= y[n];
```


```diff
+ ## 4. Replica Anti-Affinity: Replicas of the same application on different nodes

+ s.t. ReplicaAntiAffinity{a in APPLICATIONS, s1 in REPLICAS [a], s2 in REPLICAS[a], n in NODES: s1 <> s2}:
+  x[a,s1,n] + x[a,s2,n] <= 1; 
```

