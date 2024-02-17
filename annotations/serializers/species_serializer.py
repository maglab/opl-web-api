from annotations.models.species import Species, SpeciesProblem
from open_problems.serializers import OpenProblemsSerializer
from utils.base_serializer import BaseSerializer


class SpeciesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Species
        fields = "__all__"


class SpeciesProblemSerializer(BaseSerializer):
    species = SpeciesSerializer()
    open_problem = OpenProblemsSerializer()

    class Meta(BaseSerializer.Meta):
        model = SpeciesProblem
        fields = "__all__"
