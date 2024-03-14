from rest_framework import serializers

from posts_comments.models.comments import Comment


# For serializing a comment without its children
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent",
            "full_text",
            "alias",
            "created_at",
            "is_active",
        ]


# Nested recursive serializer for getting child comments
class RecursiveCommentSerializer(CommentSerializer):
    children = serializers.SerializerMethodField

    class Meta:
        model = Comment
        fields = [
            "id",
            "submission_id",
            "parent",
            "full_text",
            "created_at",
            "alias",
            "is_active",
        ]

    def get_children(self, instance):
        children_queryset = instance.children.all()
        serializer = RecursiveCommentSerializer(
            children_queryset, many=True, context=self.context
        )
        return serializer.data


class CommentsSerializer(CommentSerializer):
    children = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta(CommentSerializer.Meta):
        model = Comment
        fields = [
            "comment_id",
            "posts",
            "parent",
            "full_text",
            "children",
            "alias",
            "created_at",
            "is_active",
        ]
