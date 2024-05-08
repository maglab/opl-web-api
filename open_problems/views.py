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
from .filters import OpenProblemsFilter


class ListProblemsView(ListAPIView):
    """
    For retrieving all open problems and sort them depending on url and query parameters.
    """

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


class RetrieveProblemView(RetrieveAPIView):
    """
    Retrieve single open problem using an identifier
    """

    serializer_class: Serializer = OpenProblemsSerializer
    queryset = OpenProblem


class SubmitOpenProblemView(CreateAPIView):
    queryset = SubmittedOpenProblem.objects.all()
    serializer_class = SubmittedOpenProblemPostSerializer

    @staticmethod
    def send_confirmation_email(user_email: str): ...

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            data = set_up_data(request.data)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                # Here we check whether there is a contact
                email = serializer.data.get("email")

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
