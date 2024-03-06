from annotations.models import Compound, CompoundProblem
from annotations.serializers import (
    CompoundsSerializer,
    CompoundProblemSerializer,
)
from .annotation_view import AnnotationViewSet, AnnotationProblemViewSet


class CompoundViewSet(AnnotationViewSet):
    """Viewset for species model"""

    def __init__(self, *args, **kwargs):
        super().__init__(Compound, CompoundsSerializer, *args, **kwargs)


class CompoundProblemViewSet(AnnotationProblemViewSet):
    """Viewset for SpeciesProblem Model"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            CompoundProblem,
            CompoundProblemSerializer,
            annotation_foreign_key="compound",
        )
