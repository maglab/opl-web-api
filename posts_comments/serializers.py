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
    post = serializers.PrimaryKeyRelatedField(queryset=Solution.objects.all())

    class Meta:
        model = CommentSolution
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        post_instance = instance.post
        representation["post"] = SolutionSerializer(post_instance).data
        return representation


class CommentDiscussionSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Discussion.objects.all())

    class Meta:
        model = CommentDiscussion
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        post_instance = instance.post
        representation["post"] = DiscussionSerializer(post_instance).data
        return representation
