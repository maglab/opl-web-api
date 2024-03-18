from django.db import models
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.service.queryset_helpers import (
    get_queryset_ordered,
    get_queryset_annotated,
)
from open_problems.models import OpenProblem
from open_problems.serializers import (
    OpenProblemsSerializer,
)
from utils.Pagination import Pagination
from ..filters.open_problems import OpenProblemsFilter
from ..service.clean_query_params import clean_query_params


class RetrieveProblems(ListAPIView):
    """
    For retrieving all open problems and sort them depending on url and query parameters.
    """

    search_fields = [
        "title",
        "description",
    ]
    filterset_class = OpenProblemsFilter
    filter_backends = [SearchFilter]
    pagination_class = Pagination
    serializer_class = OpenProblemsSerializer

    @staticmethod
    def sort_queryset(queryset: QuerySet, sorting: str) -> QuerySet:
        """
        Static method for final sorting of filtered queryset. Utilises helper functions.
        Parameters:
            queryset: Model queryset
            sorting (str): Type of sorting to appy.
        """
        if sorting == "latest":
            return get_queryset_ordered(
                queryset=queryset, id_string="-problem_id", is_active=True
            )
        elif sorting == "root":
            return get_queryset_ordered(
                queryset=queryset, id_string="-problem_id", is_active=True, parent=None
            )
        elif sorting == "answered":
            return get_queryset_annotated(
                queryset=queryset,
                annotate_by={"post_count": models.Count("post")},
                id_string="-post_count",
                filters=[
                    {"post__is_active": True},
                    {"post_count__gte": 1},
                ],
            )
        elif (
            sorting == "top"
        ):  # Ordering by descendants - may not be used in the future
            return get_queryset_ordered(
                queryset=queryset, id_string="-descendants_count", is_active=True
            )
        elif sorting == "submissions":
            return get_queryset_annotated(
                queryset,
                annotate_by={"post_count": models.Count("post")},
                id_string="-post_count",
            )

    @staticmethod
    def filter_by_annotations(
        queryset: QuerySet, annotation_type: str, ids: [int]
    ) -> QuerySet:
        """
        Static method to apply filtering on queryset.
        Parameters:
            queryset (QuerySet): Django Queryset of selected model
            annotation_type (str): Annotation type referencing the model to cross-reference to with current queryset
            ids ([ids]): Array of ids to retrieve objects from given annotation model.

        Returns:
            QuerySet
        """
        # Instead we parse a string for annotation types

        if len(ids) == 0:
            return queryset
        else:
            filter_keyword = f"{annotation_type}problem__{annotation_type}__id__in"
            return queryset.filter(**{filter_keyword: ids})

    def get_queryset(self) -> QuerySet:
        """
        The queryset to be returned as the list view. Queryset is filtered by annotation and then sorted and then sorted
        at the end.
        Returns:
            Queryset
        """
        queryset = OpenProblem.objects.all()
        query_params = clean_query_params(self.request.query_params, Pagination)

        # Remove sorting and store separately as we want to sort at the end and to remove it from the annotation
        # filtering loop below.
        if "sorting" in query_params.keys():
            sorting = query_params.pop("sorting")[0]
        else:
            sorting = (
                "latest"  # Set sorting to latest as default if there is no value there
            )

        for parameter_name, parameter_value in query_params.items():
            queryset = self.filter_by_annotations(
                queryset=queryset, annotation_type=parameter_name, ids=parameter_value
            )

        queryset = self.sort_queryset(queryset, sorting)

        return queryset


class RetrieveSingleProblem(RetrieveAPIView):
    """
    Retrieve single open problem using an identifier
    """

    serializer_class: Serializer = OpenProblemsSerializer
    queryset = OpenProblem

    def get(self, request, *args, **kwargs):
        """
        Retrieve id from url path and return single object instance
        """
        object_id = self.kwargs.get("id")
        queryset = self.queryset.objects.get(problem_id=object_id)
        return Response(self.serializer_class(queryset).data, status=status.HTTP_200_OK)
