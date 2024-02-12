from ..models.open_problems import ProblemReference
from ..serializers.serializers import FilterReferenceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Get references for an open problem
@api_view(['GET'])
def get_references(request, id):
    references = ProblemReference.objects.filter(problem_id=id)
    serializer = FilterReferenceSerializer(references, many=True)
    if not references:
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
