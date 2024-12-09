# The Math behind Kubernetes - Part 1 - Introduction

In less than a decade, Kubernetes has become the most popular platform for managing containerized workloads. Thanks to its distinctive configuration syntax and the numerous tools created by the community, Kubernetes is very approachable to both developers and system administrators.

While simple to use, administrating a Kubernetes cluster presents many challenges. You learn to deal with challenges such as autoscaling, sizing nodes, assigning requests and limits, configuring probes, etc. For each problem, it is quite easy to find tools or empirical solutions. 

Quite often, solutions to sizing problems you will find over the internet rely on rules of thumb. In most cases, they make a lot of sense and provide a very good approximate solution to the problem they are trying to solve.

But my mathematical curricula could not step there. I have a background in applied Mathematics, and I previously studied Industrial engineering. The industrial world has been obsessed with finding analytical solutions to almost any operational problem. Believe it or not, many operational problems found in Kubernetes operations are the same as some classic inventory management or packing problems.

I decided to put back on my mathematical hat and look at the Kubernetes problem from another angle. It is good to occasionally look at a problem with another pair of eyes. This will probably lead to a series of articles.

In the first, I will explain what common mathematical problems you are facing when operating a Kubernetes Cluster.

## Defining the Kubernetes Cluster Sizing Problem

The goal of Kubernetes mode sizing is to find the optimal **number of nodes** and the **size of those nodes** (in terms of CPU, memory, and other resources) to run your applications. This needs to balance performance requirements with cost efficiency. 

The statement may seem simple, but in real-world scenarios, many constraints and variability need to be considered. Throughout this discussion, we will start with the most simplistic model and the most interesting constraints to the problem. Let's make some initial assumptions.

* **Application resource needs**: Each application (or pod) has desired resource requirements (CPU, memory). This desired requirement is assumed to be the pod resource requests.
* **Node types and costs**: A Cloud provider offers a finite discrete number of machine types with different resource capacities and costs.

### How to Mathematically Model this Problem?

### MIP Problem Formulation

Here's a basic MIP formulation for the Kubernetes node sizing problem. This can be further extended to include more complex scenarios.

**Sets:**

* **A**: Set of applications
* **N**: Set of available node types

**Parameters:**

* $r_{a,resource}$ : Resource requirement (CPU, memory) for application $a∈A$
* $c_{n,resource}$ : Resource Capacity (CPU, memory) for node type $n∈N$
* $cost_{n}$ : Cost of node type $n∈N$

**Decision Variables:**

* $x_{a,n}$: Binary variable, equals 1 if application a is assigned to node type n, 0 otherwise
* $y_{n}$: Integer variable, number of nodes of type n

**Objective:**

$$
\text{Minimize} \sum_{n \in \mathcal{N}} cost_n \cdot y_n 
$$

**Constraints:**

1. **Application Assignment**: Each application must be assigned to exactly one node type:

$$
\sum_{n \in \mathcal{N}} x_{a,n} = 1 \quad \forall a \in \mathcal{A}
$$

2. **Resource Capacity**: The total resource demand on a node type cannot exceed its capacity:

$$
\sum_{a \in \mathcal{A}} r_{a,resource} \cdot x_{a,n}  \le c_{n,resource} \cdot y_n \quad \forall n \in \mathcal{N}, \forall \text{ resource}
$$

3. **Node Count**: Ensure at least one node of a type is provisioned if any application is assigned to it:

$$
x_{a,n} \le y_n \quad \forall a \in \mathcal{A}, \forall n \in \mathcal{N}
$$

