def sort_query_params(query_parameters: dict) -> dict:
    sorted_parameters = {
        "pagination_number": 1,
        "annotations": None,
        "string_search": None,
    }
    for parameter, parameter_value in query_parameters.items():
        if parameter == "p":
            ...
        else:
            ...
