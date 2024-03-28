from rest_framework_filters import FilterSet, filters
from .models import Tag, Gene, GeneProblem, Species, SpeciesProblem

"""
All tags and annotations will require a FilterSet if we are to filter open problems based on these models.
"""


class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = {"title": ["exact", "in"]}


class GeneFilter(FilterSet):
    gene_name = filters.CharFilter(field_name="gene_name", lookup_expr="exact")
    gene_symbol = filters.CharFilter(field_name="gene_symbol", lookup_expr="exact")

    class Meta:
        model = Gene
        fields = ["gene_name", "gene_symbol"]


class GeneProblemFilter(FilterSet):
    gene = filters.RelatedFilter(
        GeneFilter, field_name="gene", queryset=Gene.objects.all()
    )

    class Meta:
        model = GeneProblem
