from django.db.models import Count
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from annotations.models import (
    Compound,
    Gene,
    Species,
    Tag,
)
from annotations.serializers import (
    CompoundsSerializer,
    GeneSerializer,
    SpeciesSerializer,
    TagSerializer,
)
from utils.exceptions import EmptyQuerySetError


class AnnotationViewSet(ReadOnlyModelViewSet, ListModelMixin):
    """A generic viewset for Annotation models such as Gene and Theory."""

    def __init__(self, detail_model, detail_serializer, *args, **kwargs):
        self.detail_model = detail_model
        self.queryset = detail_model.objects.all()
        self.serializer_class = detail_serializer
        super().__init__()

    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve method for getting a particular annotation"""
        try:
            instance = self.detail_model.objects.get(pk=pk)
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except self.detail_model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        """Retrieve all annotation entries"""
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CompoundViewSet(AnnotationViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(Compound, CompoundsSerializer, *args, **kwargs)
        self.queryset = Compound.objects.annotate(
            open_problem_count=Count("openproblem__compounds")
        ).order_by("-open_problem_count")


class GeneViewSet(AnnotationViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            Gene,
            GeneSerializer,
        )
        self.queryset = Gene.objects.annotate(
            open_problem_count=Count("openproblem__genes")
        ).order_by("-open_problem_count")


class SpeciesViewSet(AnnotationViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(Species, SpeciesSerializer, *args, **kwargs)
        self.queryset = Species.objects.annotate(
            open_problem_count=Count("openproblem__species")
        ).order_by("-open_problem_count")


class TagViewSet(AnnotationViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(
            Tag,
            TagSerializer,
        )
        self.queryset = Tag.objects.annotate(
            open_problem_count=Count("openproblem__tags")
        ).order_by("-open_problem_count")
