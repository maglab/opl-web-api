from annotations.models.compounds import Compounds, CompoundProblems
from .annotation_view import AnnotationViewSet, AnnotationProblemViewSet
from annotations.serializers.compound_serializer import (
    CompoundsSerializer,
    CompoundProblemSerializer,
)


class CompoundViewSet(AnnotationViewSet):
    """Viewset for species model"""

    def __init__(self, *args, **kwargs):
        super().__init__(Compounds, CompoundsSerializer, *args, **kwargs)


class CompoundProblemViewSet(AnnotationProblemViewSet):
    """Viewset for SpeciesProblem Model"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            CompoundProblems,
            CompoundProblemSerializer,
            annotation_foreign_key="compound",
        )
