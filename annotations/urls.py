from django.urls import path

from annotations.views.filter_annotations_view import filter_annotations
from annotations.views.gene_view import get_gene, get_genes
from annotations.views.theory_view import get_theories, get_theory

# Base url api/annotations/
urlpatterns = [
    path(
        "<int:id>/theory", get_theories
    ),  # Path for getting theories related to an open problem
    path(
        "theory/<int:id>", get_theory
    ),  # Path for getting a theory / category out of the database
    path("<int:id>/genes", get_genes),
    path("gene/<int:id>", get_gene),
    path("filter/", filter_annotations),
]
