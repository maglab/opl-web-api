from django_filters import FilterSet, CharFilter

from ..models.open_problems import OpenProblem


class OpenProblemsFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    description = CharFilter(lookup_expr="icontains")
    geneproblem__name = CharFilter(
        lookup_expr="icontains", field_name="geneproblem__name"
    )
    subjectproblem__title = CharFilter(
        lookup_expr="icontains", field_name="subjectproblem__title"
    )

    class Meta:
        model = OpenProblem
        fields = ["title", "description", "geneproblem__name", "subjectproblem__title"]
