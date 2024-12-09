# Solving Mix-integer Programs

A Mixed-Integer Program (MIP) is a mathematical optimization problem where some of the variables are restricted to integer values (whole numbers), while others can take on continuous values. This is in contrast to a Linear Program (LP), where all variables can be continuous.

In the Kubernetes node sizing problem, we have several decisions that require integer values:

* Number of nodes: You can't have a fraction of a node.
* Replica count: Applications typically have a whole number of replicas.
* Node type selection: In some cases, you might want to restrict the solution to use only one type of node (as we did in the previous example).

Mix-integer Programs provides su with a rigorous framework to formulate and describe any such optimization problem. But more importantly, Given enough time and resources a MIP Solver guarantee finding the optimal solution, but in many practical scenarios, finding a near-optimal solution with a small optimality gap is considered acceptable.

## Formulating a problem in MathProg

MathProg is a specialized modeling language used to describe mathematical optimization problems, particularly linear programming (LP) and mixed-integer programming (MIP) problems.

```bash
# Define variables
var x >= 0;
var y >= 0;

# Objective function
maximize z: 3*x + 2*y;

# Constraints
s.t. constraint1: 2*x + y <= 4;
s.t. constraint2: x + 2*y <= 5;

# Solve and display the solution
solve;
display x, y, z;
end;
```

## Solving the problems with GLPK

[GLPK](https://github.com/firedrakeproject/glpk) stands for GNU Linear Programming Kit. It's a free and open-source software package used for solving large-scale linear programming (LP), mixed-integer programming (MIP), and other related optimization problems. Concretely it is an implementation of common MIP resolution algorism including [simplex method](https://en.wikipedia.org/wiki/Simplex_algorithm) and [branch-and-cut method](https://en.wikipedia.org/wiki/Branch_and_cut). We won't go to much in the detail of those algorithm in this article but essential the `simplex method` is used to solve LP problems and `branch-and-cut` finds integers solution for the corresponding MIP problems.


