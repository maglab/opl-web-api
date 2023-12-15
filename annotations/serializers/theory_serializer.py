from annotations.models.theory import Theory, TheoryProblem
from annotations.serializers.base_serializer import BaseSerializer


class TheorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Theory
        fields = ["theory_title", "theory_description", "theory_id"]


class TheoryProblemSerializer(BaseSerializer):
    theory = TheorySerializer()

    class Meta(BaseSerializer.Meta):
        model = TheoryProblem
