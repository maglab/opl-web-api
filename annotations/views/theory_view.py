from rest_framework.decorators import api_view

from annotations.models.theory import Theory, TheoryProblem
from annotations.serializers.theory_serializer import (
    TheoryProblemSerializer,
    TheorySerializer,
)

from .get_annotations import get_annotation, get_annotation_details


@api_view(["GET"])
def get_theories(request, id):
    return get_annotation(id, TheoryProblem, TheoryProblemSerializer)


@api_view(["GET"])
def get_theory(request, id):
    return get_annotation_details(id, Theory, TheorySerializer)
