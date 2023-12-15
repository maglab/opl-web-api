from django.db import models
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from open_problems.models.open_problems import OpenProblems
from open_problems.serializers.OpenProblems import (
    OpenProblemsSerializer,
)
from ..utils.clean_query_params import clean_query_params
from ..utils.queryset_helpers import (
    get_queryset_ordered,
    get_queryset_annotated,
)


class RetrieveProblems(ListAPIView):
    """
    For retrieving all open problems and sort them depending on url and query parameters.
    """

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
                annotate_by={"submission_count": models.Count("submission")},
                id_string="-submission_count",
                filters=[
                    {"submission__is_active": True},
                    {"submission_count__gte": 1},
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
                annotate_by={"submission_count": models.Count("submission")},
                id_string="-submission_count",
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
        queryset = OpenProblems.objects.all()
        query_params = clean_query_params(self.request.query_params)

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
    queryset = OpenProblems

    def get(self, request, *args, **kwargs):
        """
        Retrieve id from url path and return single object instance
        """
        object_id = self.kwargs.get("id")
        queryset = self.queryset.objects.get(problem_id=object_id)
        return Response(self.serializer_class(queryset).data, status=status.HTTP_200_OK)
