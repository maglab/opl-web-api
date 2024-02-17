from annotations.models.compounds import Compounds, CompoundProblems
from open_problems.serializers.OpenProblems import OpenProblemsSerializer
from utils.base_serializer import BaseSerializer


class CompoundsSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Compounds


class CompoundProblemSerializer(BaseSerializer):
    compound = CompoundsSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta(BaseSerializer.Meta):
        model = CompoundProblems
