from rest_framework.serializers import ModelSerializer
from .models import Compound, CompoundProblem, Gene, GeneProblem, Species, SpeciesProblem, Subject, SubjectProblem
from open_problems.serializers import OpenProblemsSerializer


class CompoundsSerializer(ModelSerializer):
    class Meta:
        model = Compound
        fields = "__all__"


class CompoundProblemSerializer(ModelSerializer):
    compound = CompoundsSerializer()

    class Meta:
        model = CompoundProblem
        fields = ["compound"]


class GeneSerializer(ModelSerializer):
    class Meta:
        model = Gene
        fields = "__all__"


class GeneProblemlSerializer(ModelSerializer):
    gene = GeneSerializer()

    class Meta:
        model = GeneProblem
        fields = ["gene"]


class SpeciesSerializer(ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class SpeciesProblemSerializer(ModelSerializer):
    species = SpeciesSerializer()
    class Meta:
        model = SpeciesProblem
        fields = ["species"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectProblemSerializer(ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = SubjectProblem
        fields = ["subject"]
