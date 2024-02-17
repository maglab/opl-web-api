from annotations.models.genes import Gene, GeneProblem
from open_problems.serializers.OpenProblems import OpenProblemsSerializer
from utils.base_serializer import BaseSerializer


class GeneSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Gene
        fields = "__all__"


class GeneProblemlSerializer(BaseSerializer):
    gene = GeneSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta(BaseSerializer.Meta):
        model = GeneProblem
