from annotations.serializers.base_serializer import BaseSerializer
from annotations.models.genes import Gene, GeneProblem


class GeneSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Gene
        fields = "__all__"


class GeneProblemlSerializer(BaseSerializer):
    gene_id = GeneSerializer()

    class Meta(BaseSerializer.Meta):
        model = GeneProblem
