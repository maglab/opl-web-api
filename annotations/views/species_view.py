from annotations.models.species import Species, SpeciesProblem
from annotations.serializers.species_serializer import (
    SpeciesSerializer,
    SpeciesProblemSerializer,
)
from .annotation_view import AnnotationViewSet, AnnotationProblemViewSet


class SpeciesViewSet(AnnotationViewSet):
    """Viewset for species model"""

    def __init__(self, *args, **kwargs):
        super().__init__(Species, SpeciesSerializer, *args, **kwargs)


class SpeciesProblemViewSet(AnnotationProblemViewSet):
    """Viewset for SpeciesProblem Model"""

    def __init__(self):
        super().__init__(
            SpeciesProblem, SpeciesProblemSerializer, annotation_foreign_key="species"
        )
