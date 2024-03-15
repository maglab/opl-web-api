from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from open_problems.models import SubmittedOpenProblem
from open_problems.serializers import SubmittedOpenProblemSerializer
from ..service.create_instances import create_contact, pmid_doi_conversion


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
