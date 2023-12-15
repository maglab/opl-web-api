from rest_framework.decorators import api_view

from annotations.models.genes import Gene, GeneProblem
from annotations.serializers.gene_serializer import (
    GeneProblemlSerializer,
    GeneSerializer,
)

from .get_annotations import get_annotation, get_annotation_details


# Get genes for one open problem
@api_view(["GET"])
def get_genes(request, id):
    return get_annotation(id, GeneProblem, GeneProblemlSerializer)


@api_view(["GET"])
def get_gene(request, id):
    return get_annotation_details(id, Gene, GeneSerializer)
