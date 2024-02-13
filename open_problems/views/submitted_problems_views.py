from rest_framework.generics import ListCreateAPIView

from open_problems.models.open_problems import SubmittedOpenProblem
from open_problems.serializers import SubmittedOpenProblemSerializer
from ..service.create_instances import create_contact, pmid_doi_conversion


class SubmitOpenProblemView(ListCreateAPIView):
    queryset = SubmittedOpenProblem.objects.all()
    serializer_class = SubmittedOpenProblemSerializer

    @staticmethod
    def _extract_data(data: dict):
        return {
            "title": data["title"],
            "description": data["description"],
            "references": data["references"],
            "first_name": data["firstName"],
            "last_name": data["lastName"],
            "organisation": data["organisation"],
            "email": data["email"],
        }

    def create(self, request, *args, **kwargs):
        contact_instance = create_contact(request.data)
        reference_instances = pmid_doi_conversion(
            reference_identifiers=request.data["references"]
        )
