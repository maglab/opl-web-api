from rest_framework import serializers

from open_problems.models import Contact, SubmittedOpenProblem, OpenProblem
from utils.recursive_serializer import RecursiveSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class OpenProblemsSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    children = RecursiveSerializer(many=True, read_only=True)
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = OpenProblem
        fields = [
            "problem_id",
            "title",
            "description",
            "contact",
            "parent_problem",
            "descendants_count",
            "post_count",
            "children",
        ]

    @staticmethod
    def get_post_count(obj):
        return obj.post_set.count()


# Serializer for parent node of open problem
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenProblem
        fields = "__all__"


# Serializer for user submitted open problems
class SubmittedOpenProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedOpenProblem
        fields = "__all__"
