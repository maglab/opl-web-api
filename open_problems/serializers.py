from rest_framework import serializers

from open_problems.models import Contact, SubmittedOpenProblem, OpenProblem
from references.serializers import ReferenceSerializer
from utils.recursive_serializer import RecursiveSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


# Serializer for parent node of open problem
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenProblem
        fields = "__all__"


class OpenProblemsSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    children = RecursiveSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    solution_count = serializers.SerializerMethodField()
    discussion_count = serializers.SerializerMethodField()
    parent_problem = ParentSerializer()

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
