from django.urls import path, include
from rest_framework import routers

from annotations.models import CompoundProblem, GeneProblem,  SpeciesProblem, SubjectProblem
from annotations.serializers import CompoundsSerializer, GeneSerializer, SpeciesSerializer, SubjectSerializer
from annotations.views.annotation_view import MultiAnnotationView
from annotations.views.compounds_view import CompoundViewSet, CompoundProblemViewSet
from annotations.views.gene_view import GeneViewSet, GeneProblemViewSet
from annotations.views.species_view import SpeciesViewSet, SpeciesProblemViewSet
from annotations.views.subject_view import (
    SubjectViewSet,
    SubjectProblemViewSet,
)

# Register routers the viewsets

router = routers.DefaultRouter()
viewsets = {
    "gene": GeneViewSet,
    "subject": SubjectViewSet,
    "species": SpeciesViewSet,
    "compound": CompoundViewSet,
}

for route, viewset in viewsets.items():
    router.register(route, viewset, basename=route)

# Create a list of prefixes for the viewsets for urls to be dynamically generated
viewsets_patterns = [
    (GeneProblemViewSet, "gene"),
    (SubjectProblemViewSet, "subject"),
    (SpeciesProblemViewSet, "species"),
    (CompoundProblemViewSet, "compound"),
]

model_serializer_data = {
    "gene": (GeneProblem, GeneSerializer),
    "subject": (SubjectProblem, SubjectSerializer),
    "compound": (CompoundProblem, CompoundsSerializer),
    "species": (SpeciesProblem, SpeciesSerializer),
}


# Base url api/annotations/
urlpatterns = [
    path("", include(router.urls)),
    path(
        "all/<int:problem_id>",
        MultiAnnotationView.as_view(),
    ),
]


# Add to the urlpatterns list
# Example: {base_url}/api/annotations/{prefix/}filter/by-problem:1
# Example 2: {base_url}/api/annotations/{prefix}}filter/by-annotation:1
for viewset, prefix in viewsets_patterns:
    urlpatterns += [
        path(
            f"{prefix}/filter/by-problem:<int:problem_id>",
            viewset.as_view({"get": "get_annotations"}),
        ),
        path(
            f"{prefix}/filter/by-annotation:<int:annotation_id>",
            viewset.as_view({"get": "get_problems"}),
        ),
    ]
