import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from open_problems.serializers.serializers import (
    SubmittedProblemSerializer,
)
from utils.create_reference import create_reference


class SubmitOpenProblem(APIView):
    @staticmethod
    def convert_references(request):
        references = request.data.get("references")
        references_json = json.loads(references)

        references_dict = {}

        for ref, key in references_json.items():
            ref_type = key["type"]
            value = key["value"]
            references_dict[ref] = create_reference(ref_type, value)
        return references_dict

    def post(self, request, *args, **kwargs):
        # First convert the references - they should have already been verified by the api and client before submission
        if request.data.get("references"):
            references = self.convert_references(request)
            data = request.data
            data["references"] = json.dumps(
                references
            )  # Replace the references with the converted references
        else:
            data = request.data
        problem_serializer = SubmittedProblemSerializer(data=data)
        if problem_serializer.is_valid(raise_exception=True):
            problem_serializer.save()
            return Response(problem_serializer.data, status=status.HTTP_201_CREATED)
