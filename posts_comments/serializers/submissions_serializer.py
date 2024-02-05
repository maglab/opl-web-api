from rest_framework import serializers

from posts_comments.models.Post import (
    Post,
    PostReferences,
    SubmittedReferences,
)


class PostSerializer(serializers.ModelSerializer):
    open_problem_title = serializers.ReadOnlyField(
        source="open_problem.title"
    )  # Get the title of the open problem. For now this is the only information we need. Do not need to add
    # serializer class to the open problem FK.

    class Meta:
        model = Post
        fields = [
            "id",
            "created_at",
            "full_text",
            "contact",
            "submitted_references",
            "open_problem",
            "open_problem_title",
            "first_name",
            "last_name",
            "affiliation",
        ]


class PostReferencesSerializer(serializers.ModelSerializer):
    references = serializers.SerializerMethodField()

    class Meta:
        model = PostReferences
        fields = ["post_id", "reference_id", "references"]

    def get_references(self, obj):
        reference = obj.reference_id
        return {
            "id": reference.id,
            "full_citation": reference.citation,
        }


class SubmittedReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedReferences
        fields = ["reference_id", "submission_id", "type", "ref"]
