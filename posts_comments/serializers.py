from rest_framework import serializers
from references.serializers import ReferenceSerializer
from .models import Solution, Discussion, Comment


# Posts
class PostSerializer(serializers.ModelSerializer):
    open_problem_title = serializers.ReadOnlyField(source="open_problem.title")
    references = ReferenceSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"


class SolutionSerializer(PostSerializer):
    class Meta:
        model = Solution
        fields = "__all__"


class DiscussionSerializer(PostSerializer):
    class Meta:
        model = Discussion
        fields = "__all__"


# Comments
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


# Nested recursive serializer for getting child comments
class RecursiveCommentSerializer(CommentSerializer):
    children = serializers.SerializerMethodField

    class Meta:
        model = Comment

    def get_children(self, instance):
        children_queryset = instance.children.all()
        serializer = RecursiveCommentSerializer(
            children_queryset, many=True, context=self.context
        )
        return serializer.data
