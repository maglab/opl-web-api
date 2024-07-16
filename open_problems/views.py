import os
import datetime as dt

from django.db.models import QuerySet
from django.db import transaction

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django_filters.rest_framework import DjangoFilterBackend

from open_problems.models import OpenProblem, SubmittedOpenProblem
from .service.submit_service import SubmitOpenProblemService
from open_problems.serializers import (
    OpenProblemsSerializer,
    SubmittedOpenProblemPostSerializer,
)
from core.utils.Pagination import Pagination
from .filters import OpenProblemsFilter
from core.emails import (
    EmailExtractor,
    MailtrapTemplateEmailSender,
    MailtrapConfigurator,
    get_templates,
)


MAILTRAP_TOKEN = os.environ.get("MAILTRAP_API_KEY")


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
    email_client = MailtrapConfigurator(token=MAILTRAP_TOKEN)
    email_templates = get_templates()

    def set_up_email_contents(self, request_data: dict):
        template = self.email_templates.get("submit_open_problem")
        uuid = template.get("uuid")
        user_name, email = EmailExtractor.extract(data=request_data)
        template_variables = template.get("template_variables")
        template_variables["contact"] = user_name
        template_variables["year"] = dt.datetime.now().year
        return uuid, user_name, email, template_variables

    def send_confirmation_email(self, uuid: str, email: str, template_variables: dict):
        configured_client = self.email_client.configure_client()
        sender = MailtrapTemplateEmailSender(client=configured_client)
        sender.send_email(
            to_email=email, template_uuid=uuid, template_variables=template_variables
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            data = SubmitOpenProblemService(request=request.data).create()
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                if not serializer.validated_data.get(
                    "email"
                ) or not serializer.validated_data.get("notify_user"):
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                uuid, user_name, email, template_variables = self.set_up_email_contents(
                    request_data=request.data
                )
                self.send_confirmation_email(
                    uuid=uuid,
                    email=email,
                    template_variables=template_variables,
                )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                data={"error": f"Caught error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
