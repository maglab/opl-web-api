from rest_framework.serializers import ModelSerializer, SerializerMethodField
from utils.serializers import AllFieldsSerializer
from .models import (
    Compound,
    Gene,
    Species,
    Tag,
)


class CompoundsSerializer(AllFieldsSerializer):
    class Meta(AllFieldsSerializer.Meta):
        model = Compound


class GeneSerializer(AllFieldsSerializer):
    class Meta(AllFieldsSerializer.Meta):
        model = Gene


class SpeciesSerializer(AllFieldsSerializer):
    full_name = SerializerMethodField(read_only=True)

    @staticmethod
    def get_full_name(obj):
        return f"{obj.genus} {obj.species}"

    class Meta(AllFieldsSerializer.Meta):
        model = Species


class TagSerializer(AllFieldsSerializer):
    class Meta(AllFieldsSerializer.Meta):
        model = Tag
