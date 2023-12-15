from rest_framework.request import Request


def clean_query_params(query_params: Request) -> dict:
    """
    Returns cleaned query params from the client. Django will append '[]' when object attributes containing arrays are
    serialized. These are removed and the multiple entries of ids are concatenated together into one array.

    Parameters:
        query_params (dict): A dictionary received from a Django get request containing query parameters
    Optional parameters:
        **kwargs (string): String to remove any data from the query params.
    """
    cleaned_param_dict: dict = {}
    for key in query_params.keys():
        cleaned_key = key.strip("[]")
        array = query_params.getlist(key)
        cleaned_param_dict[cleaned_key] = array
    return cleaned_param_dict
