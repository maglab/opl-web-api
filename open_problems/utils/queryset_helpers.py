from django.db.models import QuerySet

"""
Helper functions for retrieving open problems
"""


def get_queryset_ordered(queryset: QuerySet, id_string: str, **kwargs) -> QuerySet:
    """
    Returns a queryset based on the ids of the queryset in descending or ascending order.
    (-id_string = descending, id_string = ascending)

    Parameters:
        queryset (QuerySet): Django queryset
        id_string (str): The field name of the ID string
    Optional Parameters:
    **kwargs: Optional filtering parameters on the queryset

    Returns:
        Queryset
    """
    return queryset.filter(**kwargs).order_by(id_string)


def get_queryset_annotated(
    queryset: QuerySet, annotate_by: dict, id_string: str, filters: [dict] = None
) -> QuerySet:
    """
    Returned annotated and possibly filtered queryset.
    {
    parameters: [],
    value: [],
    }
    Parameters:
        queryset (QuerySet): Django queryset
        annotate_by (dict): To annotate the query by {param:val}
        id_string (str): Identifying field string to order the queryset by
        filters ([dict]): {parameter:value} - Allows for chaining of filters and conditions. (Optional)

    """
    queryset = queryset.annotate(**annotate_by)
    # Annotate first, filter then order queryset before returning.
    if filters:
        for filter_dictionary in filters:
            queryset = queryset.filter(**filter_dictionary)
    queryset = queryset.order_by(id_string)

    return queryset
