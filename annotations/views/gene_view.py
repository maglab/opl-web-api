from annotations.models.genes import Gene, GeneProblem
from annotations.serializers.gene_serializer import (
    GeneProblemlSerializer,
    GeneSerializer,
)
from .annotation_view import AnnotationViewSet, AnnotationProblemViewSet


# Class view using inherited view set
class GeneViewSet(AnnotationViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            Gene,
            GeneSerializer,
        )


class GeneProblemViewSet(AnnotationProblemViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(GeneProblem, GeneProblemlSerializer, "gene_id")
