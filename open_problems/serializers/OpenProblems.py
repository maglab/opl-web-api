from rest_framework import serializers
from open_problems.models.open_problems import OpenProblems
from utils.recursive_serializer import RecursiveSerializer


class OpenProblemsSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = OpenProblems
        fields = ["problem_id", "title", "description",
                  "contact", "parent_problem", "descendants_count", "submission_count", "children"]

    def get_submission_count(self, obj):
        return obj.submission_set.count()


class DescendantsDescendingSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = OpenProblems
        fields = ["problem_id", "title", "description",
                  "contact", "parent_problem", "descendants_count", "children"]

    def get_children(self, instance):
        ordered_children = instance.children.all().order_by('-descendants_count')
        serializer = DescendantsDescendingSerializer(
            ordered_children, many=True, context=self.context)
        return serializer.data


class DescendantsAscendingSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = OpenProblems
        fields = ["problem_id", "title", "description",
                  "contact", "parent_problem", "descendants_count", "children"]

    def get_children(self, instance):
        ordered_children = instance.children.all().order_by('descendants_count')
        serializer = DescendantsDescendingSerializer(
            ordered_children, many=True, context=self.context)
        return serializer.data
