from rest_framework import serializers

from open_problems.models import Contact, SubmittedOpenProblem, OpenProblem
from references.serializers import ReferenceSerializer
from annotations.serializers import (
    TagSerializer,
    GeneSerializer,
    CompoundsSerializer,
    SpeciesSerializer,
)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


# Serializer for parent node of open problem
class ParentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenProblem
        fields = ["title", "problem_id", "description"]


class OpenProblemsSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    children = ParentChildSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    solution_count = serializers.SerializerMethodField()
    discussion_count = serializers.SerializerMethodField()
    parent_problem = ParentChildSerializer()
    tags = TagSerializer(many=True, read_only=True)
    genes = GeneSerializer(many=True, read_only=True)
    compounds = CompoundsSerializer(many=True, read_only=True)
    species = SpeciesSerializer(many=True, read_only=True)

    class Meta:
        model = OpenProblem
        fields = [
            "problem_id",
            "title",
            "description",
            "contact",
            "parent_problem",
            "references",
            "descendants_count",
            "solution_count",
            "children",
            "discussion_count",
            "tags",
            "genes",
            "compounds",
            "species",
        ]

    @staticmethod
    def get_solution_count(obj):
        return obj.solution.count()

    @staticmethod
    def get_discussion_count(obj):
        return obj.discussion.count()


# Serializer for user submitted open problems
class SubmittedOpenProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedOpenProblem
        fields = "__all__"
