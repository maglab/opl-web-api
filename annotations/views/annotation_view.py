from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from annotations.models.compounds import CompoundProblems
from annotations.models.genes import GeneProblem
from annotations.models.species import SpeciesProblem
from annotations.models.subjects import SubjectProblem
from annotations.serializers.compound_serializer import CompoundProblemSerializer
from annotations.serializers.gene_serializer import GeneProblemlSerializer
from annotations.serializers.species_serializer import SpeciesProblemSerializer
from annotations.serializers.subject_serializer import SubjectProblemSerializer
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


class AnnotationProblemViewSet(ReadOnlyModelViewSet):
    """A viewset for intermediate models linking an annotation and open problem. eg. GeneProblem model"""

    def __init__(
        self,
        intermediate_model,
        intermediate_serializer,
        annotation_foreign_key,
        *args,
        **kwargs
    ):
        self.intermediate_model = intermediate_model
        self.queryset = intermediate_model.objects.all()
        self.serializer_class = intermediate_serializer
        self.annotation_foreign_key = annotation_foreign_key
        super().__init__()

    def get_annotations(self, request, *args, **kwargs):
        """Viewset method for returning an annotation or annotations for a particular open problem"""
        problem_id = kwargs.get("problem_id")
        try:
            filtered_results = self.intermediate_model.objects.filter(
                open_problem_id=problem_id
            )
            if not filtered_results.exists():
                raise EmptyQuerySetError

        except EmptyQuerySetError as e:
            return Response(str(e), status=status.HTTP_204_NO_CONTENT)

        else:
            serializer = self.serializer_class(filtered_results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_problems(self, request, *args, **kwargs):
        """Viewset method for returning an open problem or open problems for a particular annotation"""

        annotation_id = kwargs.get("annotation_id")
        try:

            filtered_results = self.intermediate_model.objects.filter(
                **{self.annotation_foreign_key: annotation_id}
            )
            if not filtered_results.exists():
                raise EmptyQuerySetError

        except EmptyQuerySetError as e:
            return Response(str(e), status=status.HTTP_204_NO_CONTENT)

        else:
            serializer = self.serializer_class(filtered_results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class MultiAnnotationView(APIView):
    """
    A view for retrieving all annotations tied to an open problem.
    """

    models_serializers = {
        "gene": (GeneProblem, GeneProblemlSerializer),
        "subject": (SubjectProblem, SubjectProblemSerializer),
        "compound": (CompoundProblems, CompoundProblemSerializer),
        "species": (SpeciesProblem, SpeciesProblemSerializer),
    }

    def get(self, request, problem_id: int):
        data = {}
        for key, value in self.models_serializers.items():
            annotation_name = key
            intermediary_model, serializer = value
            queryset = intermediary_model.objects.filter(open_problem=problem_id)
            data[annotation_name] = serializer(
                queryset, many=True, context={"request": request}
            ).data
        return Response(data, status=status.HTTP_200_OK)