from knsp.models.knsp_2_auto_scaling import solve_2_knsp

# Example Usage (data from the MathProg model)
problem_data = {
    "applications": [
        "web-server",
        "api-gateway",
        "batch-processor",
        "message-queue",
        "cache-service",
        "database-replica",
        "streaming-analytics",
        "machine-learning-inference",
        "reporting-service",
        "data-warehouse-loader",
    ],
    "resources": ["cpu", "memory"],
    "node_types": [
        "c4-standard-2",
        "c4-standard-4",
        "c4-standard-8",
        "c4-highcpu-2",
        "c4-highcpu-4",
        "c4-highcpu-8",
        "c4-highmem-2",
        "c4-highmem-4",
        "c4-highmem-8",
    ],
    "time_intervals": 24,
    "replicas": {
        "web-server":                 [2, 2, 2, 2, 2, 2, 2, 3, 5, 6, 7, 8, 10, 8, 7, 6, 5, 6, 8, 6, 5, 4, 3, 2],
        "api-gateway":                [2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 5, 5, 6, 5, 4, 4, 3, 3, 5, 4, 3, 2, 2, 2],
        "batch-processor":            [3, 3, 2, 2, 2, 2, 3, 4, 6, 7, 8, 8, 10, 8, 7, 7, 6, 7, 9, 7, 6, 5, 4, 3],
        "message-queue":              [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 4, 3, 3, 3, 3, 4, 3, 3, 2, 2, 2],
        "cache-service":              [2, 2, 2, 2, 2, 2, 2, 3, 4, 5, 6, 6, 8, 7, 6, 5, 5, 5, 7, 6, 5, 4, 3, 2],
        "database-replica":           [2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 3, 3, 3, 2, 2, 3, 3, 2, 2, 2, 2],
        "streaming-analytics":        [2, 2, 2, 2, 2, 2, 2, 3, 4, 5, 5, 6, 7, 6, 6, 5, 5, 6, 7, 6, 5, 4, 3, 2],
        "machine-learning-inference": [2, 2, 2, 2, 2, 3, 3, 4, 5, 6, 7, 7, 8, 7, 6, 6, 5, 5, 7, 6, 5, 4, 3, 2],
        "reporting-service":          [2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 5, 6, 5, 4, 4, 4, 4, 5, 4, 3, 3, 2, 2],
        "data-warehouse-loader":      [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 4, 4, 3, 3, 3, 4, 3, 3, 2, 2, 2],
    },
    "r": {
        # scaling 1000 -> mcore, mb
        "web-server":                 {"cpu": 250, "memory": 500},
        "api-gateway":                {"cpu": 500,  "memory": 1000},
        "batch-processor":            {"cpu": 750, "memory": 1500},
        "message-queue":              {"cpu": 500,  "memory": 1000},
        "cache-service":              {"cpu": 250, "memory": 500},
        "database-replica":           {"cpu": 1000,  "memory": 2000},
        "streaming-analytics":        {"cpu": 500,  "memory": 1000},
        "machine-learning-inference": {"cpu": 750, "memory": 2000},
        "reporting-service":          {"cpu": 1000,  "memory": 4000},
        "data-warehouse-loader":      {"cpu": 2500, "memory": 1000},
    },
    "c": {
        "c4-standard-2": {"cpu": 2000, "memory": 7000},
        "c4-standard-4": {"cpu": 4000, "memory": 15000},
        "c4-standard-8": {"cpu": 8000, "memory": 30000},
        "c4-highcpu-2":  {"cpu": 2000, "memory": 4000},
        "c4-highcpu-4":  {"cpu": 4000, "memory": 8000},
        "c4-highcpu-8":  {"cpu": 8000, "memory": 16000},
        "c4-highmem-2":  {"cpu": 2000, "memory": 15000},
        "c4-highmem-4":  {"cpu": 4000, "memory": 31000},
        "c4-highmem-8":  {"cpu": 8000, "memory": 62000},
    },
    "cost": {
        # scaling 1000
        "c4-standard-2": 969,
        "c4-standard-4": 1977,
        "c4-standard-8": 3953,
        "c4-highcpu-2":  851,
        "c4-highcpu-4":  1701,
        "c4-highcpu-8":  3402,
        "c4-highmem-2":  1284,
        "c4-highmem-4":  2607,
        "c4-highmem-8":  5214,
    },
}

# Solve with application placement, replicas, and time intervals
optimal_cost, assignment, node_counts = solve_2_knsp(problem_data)

if optimal_cost is not None:
    print(f"Total cost: {optimal_cost}")
    for t in range(problem_data["time_intervals"]):
        print(f"----- t{t} -----")
        for n in problem_data["node_types"]:
            print(f"Nodes of type {n} used: {node_counts[t][n]}")
            for i, apps in enumerate(assignment[t][n]):
                if apps:
                    print(f"  Node {i+1}: {', '.join(apps)}")
else:
    print("No feasible solution found.")
