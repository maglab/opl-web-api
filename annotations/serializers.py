from rest_framework.serializers import ModelSerializer
from .models import (
    Compound,
    Gene,
    Species,
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


class GeneSerializer(ModelSerializer):
    class Meta:
        model = Gene
        fields = "__all__"


class SpeciesSerializer(ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
