from rest_framework.serializers import ModelSerializer
from .models import (
    Compound,
    CompoundProblem,
    Gene,
    GeneProblem,
    Species,
    SpeciesProblem,
    Tag,
)


class AnnotationProblemSerializer(ModelSerializer):
    related_field = None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        related_instance = data.pop(self.related_field)
        return related_instance


class CompoundsSerializer(ModelSerializer):
    class Meta:
        model = Compound
        fields = "__all__"


class CompoundProblemSerializer(AnnotationProblemSerializer):
    compound = CompoundsSerializer()
    related_field = "compound"

    class Meta:
        model = CompoundProblem
        fields = ["compound"]


class GeneSerializer(ModelSerializer):
    class Meta:
        model = Gene
        fields = "__all__"


class GeneProblemlSerializer(AnnotationProblemSerializer):
    gene = GeneSerializer()
    related_field = "gene"

    class Meta:
        model = GeneProblem
        fields = ["gene"]


class SpeciesSerializer(ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class SpeciesProblemSerializer(AnnotationProblemSerializer):
    species = SpeciesSerializer()
    related_field = "species"

    class Meta:
        model = SpeciesProblem
        fields = ["species"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
