from django.db.models import Q
from django_filters import FilterSet, filters
from annotations.models import Tag, Gene
from .models import OpenProblem


class OpenProblemsFilter(FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags",
        to_field_name="titles",
        conjoined=True,
        label="tags",
    )

    # gene_problem_set is part of django naming convention
    gene = filters.ModelMultipleChoiceFilter(
        queryset=Gene.objects.all(),
        field_name="geneproblem__gene__gene_name",  # Adjust based on how you want to filter
        to_field_name="gene_name",  # This tells the filter to match the input against the gene_name field
        label="Gene",
    )

    class Meta:
        model = OpenProblem
        fields = ["title", "tags", "gene"]
