from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import (
    Compound,
    Gene,
    Species,
    Tag,
)


class AnnotationSerializer(ModelSerializer):
    open_problem_count = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"


class CompoundsSerializer(AnnotationSerializer):
    class Meta(AnnotationSerializer.Meta):
        model = Compound

    def create(self, validated_data: dict):
        print("test")
        instance, created = Compound.objects.get_or_create(**validated_data)
        return instance


class SpeciesSerializer(AnnotationSerializer):
    full_name = SerializerMethodField(read_only=True)

    class Meta(AnnotationSerializer.Meta):
        model = Species

    @staticmethod
    def get_full_name(obj):
        return f"{obj.genus} {obj.species}"

    def create(self, validated_data: dict):
        instance, created = Species.objects.get_or_create(**validated_data)
        return instance


class GeneSerializer(AnnotationSerializer):
    species = SpeciesSerializer()

    class Meta(AnnotationSerializer.Meta):
        model = Gene

    def create(self, validated_data: dict):
        instance, created = Gene.objects.get_or_create(**validated_data)
        return instance


class TagSerializer(AnnotationSerializer):
    class Meta(AnnotationSerializer.Meta):
        model = Tag

    def create(self, validated_data):
        instance, created = Tag.objects.get_or_create(**validated_data)
        return instance
