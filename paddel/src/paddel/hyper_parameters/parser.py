from itertools import product


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def expand_rules(parameter_rules):
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


def matches(conditions, other_conditions):
    return conditions.items() > other_conditions.items()


def merge_parameters(one, other):
    one = one.copy()
    for key in other:
        if key in one:
            one[key] += other[key]
        else:
            one[key] = other[key]

    return one


def parse_hyper_parameters(parameter_rules, prefix=""):
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
