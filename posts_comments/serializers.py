from rest_framework import serializers
from references.serializers import ReferenceSerializer
from .models import Solution, Discussion, CommentSolution, CommentDiscussion


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
class CommentSolutionSerializer(serializers.ModelSerializer):
    post = SolutionSerializer()

    class Meta:
        model = CommentSolution
        fields = "__all__"


class CommentDiscussionSerializer(serializers.ModelSerializer):
    post = DiscussionSerializer()

    class Meta:
        model = CommentDiscussion
        fields = "__all__"
