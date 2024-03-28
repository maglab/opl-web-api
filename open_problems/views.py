from django.db.models import QuerySet
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django_filters.rest_framework import DjangoFilterBackend
from open_problems.models import OpenProblem, SubmittedOpenProblem
from open_problems.serializers import (
    OpenProblemsSerializer,
    SubmittedOpenProblemSerializer,
)
from utils.Pagination import Pagination
from references.serializers import ReferenceSerializer
from .filters import OpenProblemsFilter
from .service.create_instances import create_contact, pmid_doi_conversion


class RetrieveProblems(ListAPIView):
    """
    For retrieving all open problems and sort them depending on url and query parameters.
    """

    search_fields = [
        "title",
        "description",
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OpenProblemsFilter
    pagination_class = Pagination
    serializer_class = OpenProblemsSerializer

    def get_queryset(self) -> QuerySet:
        """
        Use custom manager to sort open problems via query parameter.
        """
        queryset = (
            super().get_queryset()
        )  # Starts with the base queryset, this should trigger filtering.
        sorting = self.request.query_params.get("sorting", None)

        if sorting == "latest":
            queryset = OpenProblem.objects.latest()
        elif sorting == "root":
            queryset = OpenProblem.objects.root()
        elif sorting == "answered":
            queryset = OpenProblem.objects.answered()
        elif sorting == "top":  # Probably unecessary
            queryset = OpenProblem.objects.top()

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


class ListReferencesView(ListAPIView):
    """
    List view to list all references for an open problem.
    """

    serializer_class = ReferenceSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        open_problem = OpenProblem.objects.get(pk=pk)
        return open_problem.references.all()


class SubmitOpenProblemView(ListCreateAPIView):
    queryset = SubmittedOpenProblem.objects.all()
    serializer_class = SubmittedOpenProblemSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # Create necessary instances
                contact_instance = create_contact(data=request.data)
                converted_references, unconverted_references = pmid_doi_conversion(
                    reference_identifiers=request.data["references"]
                )
                request.data["references"] = converted_references
                request.data["contact"] = (
                    contact_instance.pk if contact_instance else None
                )
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while processing the request. {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
