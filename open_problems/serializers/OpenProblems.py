from rest_framework import serializers

from open_problems.models.open_problems import OpenProblems
from utils.recursive_serializer import RecursiveSerializer


class OpenProblemsSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = OpenProblems
        fields = [
            "problem_id",
            "title",
            "description",
            "contact",
            "parent_problem",
            "descendants_count",
            "submission_count",
            "children",
        ]

    @staticmethod
    def get_submission_count(obj):
        return obj.submission_set.count()
