from rest_framework.serializers import ModelSerializer

from .models import Category
from open_problems.models import OpenProblem


class CategoryOpenProblemSerializer(ModelSerializer):
    class Meta:
        fields = ["problem_id", "title"]
        model = OpenProblem


class CategorySerializer(ModelSerializer):
    open_problems = CategoryOpenProblemSerializer(
        many=True, read_only=True, source="get_sorted_open_problems"
    )

    class Meta:
        model = Category
        fields = "__all__"

    def get_parent(self, obj):
        if obj.parent:
            return CategorySerializer(obj.parent, context=self.context).data
        return None

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True, context=self.context).data
