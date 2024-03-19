from rest_framework.views import APIView

from annotations.models.tags import Tag, TagProblem
from annotations.serializers import (
    TagProblemSerializer,
    TagSerializer,
)
from .annotation_view import AnnotationViewSet, AnnotationProblemViewSet


class TagViewSet(AnnotationViewSet):
    """Viewset for Theory model"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            Tag,
            TagSerializer,
        )


class TagProblemViewset(AnnotationProblemViewSet):
    """Viewset for TheoryProblem model"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            TagProblem,
            TagProblemSerializer,
            annotation_foreign_key="tag",
        )
