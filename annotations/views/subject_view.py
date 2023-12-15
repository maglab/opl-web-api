from rest_framework.views import APIView
from .annotation_view import AnnotationViewSet, AnnotationProblemViewSet
from annotations.models.subjects import Subject, SubjectProblem
from annotations.serializers.subject_serializer import (
    SubjectProblemSerializer,
    SubjectSerializer,
)


class SubjectViewSet(AnnotationViewSet):
    """Viewset for Theory model"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            Subject,
            SubjectSerializer,
        )


class SubjectProblemViewSet(AnnotationProblemViewSet):
    """Viewset for TheoryProblem model"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            SubjectProblem,
            SubjectProblemSerializer,
            annotation_foreign_key="subject_id",
        )


class AnnotationProblemReferencesView(APIView):
    def __init__(self):
        super().__init__()

    """ View for obtaining all the references from all open problems under a specific annotation """
    # Do we need this?

    def get(self):
        ...
