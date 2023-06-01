from itertools import product


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def expand_rules(parameter_rules: list) -> dict:
    """Converts list of conditions and options to a dictionary that is easier to
    parse.

    Args:
        parameter_rules (list): Rules to expand.

    Returns:
        dict: Expanded rules.
    """
    expanded_rules = {}

    for conditions, parameters in parameter_rules:
        for values in product(*conditions.values()):
            simple_conditions = HashableDict(
                zip(conditions.keys(), [tuple([v]) for v in values])
            )

            if simple_conditions not in expanded_rules:
                expanded_rules[simple_conditions] = {}

            expanded_rules[simple_conditions].update(parameters)

    return expanded_rules


def matches(conditions: dict, other_conditions: dict) -> bool:
    """Determines if a condition dictionary matches within another.

    Args:
        conditions (dict): Conditions to match.
        other_conditions (dict): Conditions to match with.

    Returns:
        bool: If condition matches.
    """
    return conditions.items() > other_conditions.items()


def merge_parameters(one: dict, other: dict) -> dict:
    """Merge parameters from one dict to another.

    Args:
        one (dict): Dict to merge into.
        other (dict): Dict to merge from.

    Returns:
        dict: Merged dictionary.
    """
    one = one.copy()
    for key in other:
        if key in one:
            one[key] += other[key]
        else:
            one[key] = other[key]

    return one


def parse_hyper_parameters(parameter_rules: list, prefix="") -> list:
    """Parses custom formatted parameter rules to sklearn compatible parameter grid.

    Args:
        parameter_rules (list): Parameter rules.
        prefix (str, optional): Prefix to be used when naming the parameters. Useful when working with pipelines. Defaults to "".

    Returns:
        list: Parameter grid.
    """
    parameter_rules = expand_rules(parameter_rules)

    param_grid = []

    for conditions in parameter_rules:
        parameters = parameter_rules[conditions].copy()
        for other_conditions in parameter_rules:
            if matches(conditions, other_conditions):
                parameters = merge_parameters(
                    parameters, parameter_rules[other_conditions]
                )

        parameters.update({k: list(v) for k, v in conditions.items()})

        param_grid.append(parameters)

    # Rename to match model if using pipeline
    for params in param_grid:
        for key in list(params):
            params[f"{prefix}{key}"] = params.pop(key)

    return param_grid
