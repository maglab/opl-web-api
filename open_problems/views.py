from django.db.models import QuerySet
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django_filters.rest_framework import DjangoFilterBackend
from open_problems.models import OpenProblem, SubmittedOpenProblem
from .service.submit_service import set_up_data
from open_problems.serializers import (
    OpenProblemsSerializer,
    SubmittedOpenProblemPostSerializer,
)
from utils.Pagination import Pagination
from references.serializers import ReferenceSerializer
from .filters import OpenProblemsFilter


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
    queryset = OpenProblem.objects.all()

    def get_queryset(self) -> QuerySet:
        """
        Use custom manager to sort open problems via query parameter.
        """
        queryset = super().get_queryset()
        # Starts with the base queryset, this should trigger filtering.
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


class SubmitOpenProblemView(CreateAPIView):
    queryset = SubmittedOpenProblem.objects.all()
    serializer_class = SubmittedOpenProblemPostSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                data = set_up_data(request.data)
                print(data)
                serializer = self.serializer_class(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        data={f"error": f"Invalid data sent to endpoint"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                return Response(
                    data={"error": f"Caught error {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
