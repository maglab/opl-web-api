from rest_framework_filters import FilterSet, filters
from annotations.filters import TagFilter, GeneProblemFilter
from annotations.models import Tag, GeneProblem
from .models import OpenProblem


class OpenProblemsFilter(FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    tags = filters.RelatedFilter(TagFilter, field_name="tags", queryset=Tag)
    # gene_problem_set is part of django naming convention
    gene_problem = filters.RelatedFilter(
        GeneProblemFilter,
        field_name="geneproblem_set",
        queryset=GeneProblem.objects.all(),
    )

    class Meta:
        model = OpenProblem
