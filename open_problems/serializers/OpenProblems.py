from rest_framework import serializers

from open_problems.models.open_problems import OpenProblem
from utils.recursive_serializer import RecursiveSerializer


class OpenProblemsSerializer(serializers.ModelSerializer):
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
