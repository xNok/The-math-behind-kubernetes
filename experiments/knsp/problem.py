from typing import TypedDict, List, Dict

class ProblemData(TypedDict):
    # The resources we are optimizing for (eg. CPU, Memory)
    resource_types: List[str]
    # The set of VM type available
    node_types: List[str]
    # The resource capacity provided for a given node type
    node_capacity: Dict[str, Dict[str, int]]
    # The hourly cost of a node type
    node_cost: Dict[str, int]
    # List of application that need to be allocated to the cluster
    application_types: List[str]
    # Resource reserved by a given application
    applications_requests: Dict[str, Dict[str, int]]
    # Number of replicas for a given application
    applications_replicas: Dict[str, int]
