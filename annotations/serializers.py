from rest_framework.serializers import ModelSerializer
from .models import Compound, CompoundProblem, Gene, GeneProblem, Species, SpeciesProblem, Subject, SubjectProblem
from open_problems.serializers import OpenProblemsSerializer


class CompoundsSerializer(ModelSerializer):
    class Meta:
        model = Compound
        fields = "__all__"


class CompoundProblemSerializer(ModelSerializer):
    compound = CompoundsSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta:
        model = CompoundProblem
        fields = "__all__"


class GeneSerializer(ModelSerializer):
    class Meta:
        model = Gene
        fields = "__all__"


class GeneProblemlSerializer(ModelSerializer):
    gene = GeneSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta:
        model = GeneProblem


class SpeciesSerializer(ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class SpeciesProblemSerializer(ModelSerializer):
    species = SpeciesSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta:
        model = SpeciesProblem
        fields = "__all__"


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ["title", "description", "id", "parent"]


class SubjectProblemSerializer(ModelSerializer):
    subject = SubjectSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta:
        model = SubjectProblem
