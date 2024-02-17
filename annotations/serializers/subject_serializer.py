from annotations.models.subjects import Subject, SubjectProblem
from open_problems.serializers.OpenProblems import OpenProblemsSerializer
from utils.base_serializer import BaseSerializer


class SubjectSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Subject
        fields = ["title", "description", "id", "parent"]


class SubjectProblemSerializer(BaseSerializer):
    subject = SubjectSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta(BaseSerializer.Meta):
        model = SubjectProblem
