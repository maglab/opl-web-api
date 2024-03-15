from rest_framework import serializers

from posts_comments.models import (
    Solution,
)
from references.serializers import ReferenceSerializer


class SolutionSerializer(serializers.ModelSerializer):
    open_problem_title = serializers.ReadOnlyField(
        source="open_problem.title"
    )  # Get the title of the open problem. For now this is the only information we need. Do not need to add
    # serializer class to the open problem FK.
    references = ReferenceSerializer()

    class Meta:
        model = Solution
        fields = "__all__"
