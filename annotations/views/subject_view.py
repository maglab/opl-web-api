from rest_framework.views import APIView

from annotations.models.tags import Tag
from annotations.serializers import (
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
