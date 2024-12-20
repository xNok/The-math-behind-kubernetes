from typing import Any, List, Union, Tuple, Callable, Dict

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

# Type alias for the dimensions list
Dimensions = List[Union[
    List[Any],  # For dimensions that are lists of values
    List[str],
    Tuple[Any, ...],
    Callable[[Tuple[Any, ...]], List[int]]  # For dimensions that are functions of parent keys
]]

def create_nested_variables(
        model: cp_model.CpModel,
        dimensions: Dimensions,
        variable_name: str,
        prefix: str = "",
        parent_keys: Tuple[Any, ...] = ()
) -> IntVar | dict[Any, Any]:
    """
    Recursively creates nested dictionaries of variables.

    Args:
        model: The CP-SAT model.
        dimensions: A list representing the dimensions for nesting.
        variable_name: The base name of the variable.
        prefix: A prefix to use for naming variables in nested levels.
        parent_keys: Tuple of keys from parent dimensions.

    Returns:
        A nested dictionary of variables.
    """

    if not dimensions:
        var_name = f"{variable_name}{prefix}" if prefix else variable_name
        return model.NewBoolVar(var_name)

    current_dimension = dimensions[0]
    remaining_dimensions = dimensions[1:]

    variables: Dict[Any, Any] = {}

    if callable(current_dimension):
        keys = current_dimension(parent_keys)
        for key in keys:
            new_prefix = f"{prefix}[{key}]" if prefix else str(key)
            variables[key] = create_nested_variables(
                model,
                remaining_dimensions,
                variable_name,
                new_prefix,
                parent_keys + (key,)  # Pass down the key to the next level
            )

    elif isinstance(current_dimension, list) and current_dimension and isinstance(current_dimension[0], str):
        for key in current_dimension:
            new_prefix = f"{prefix}[{key}]" if prefix else f"[{key}]"
            variables[key] = create_nested_variables(
                model,
                remaining_dimensions,
                variable_name,
                new_prefix,
                parent_keys + (key,)  # Pass down the key to the next level
            )

    else:
        for i, _ in enumerate(current_dimension):
            new_prefix = f"{prefix}[{i}]" if prefix else f"[{i}]"
            variables[i] = create_nested_variables(
                model,
                remaining_dimensions,
                variable_name,
                new_prefix,
                parent_keys + (i,)  # Pass down the index to the next level
            )
    return variables
