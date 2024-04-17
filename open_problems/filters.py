from django.db.models import Q
from django import forms
from django_filters import FilterSet, filters
from annotations.models import Tag, Gene, Species
from references.models import Reference
from .models import OpenProblem


class OpenProblemsFilter(FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags",
        to_field_name="title",
        conjoined=True,
        label="tags",
    )

    # gene_problem_set is part of django naming convention
    gene = filters.ModelMultipleChoiceFilter(
        queryset=Gene.objects.all(),
        field_name="geneproblem__gene__gene_symbol",  # Adjust based on how you want to filter
        to_field_name="gene_symbol",  # This tells the filter to match the input against the gene_name field
        label="Gene",
        conjoined=True,
    )
    doi = filters.ModelMultipleChoiceFilter(
        queryset=Reference.objects.all(),
        field_name="references__doi",
        to_field_name="doi",
        label="reference doi",
        conjoined=True,
    )
    # Make custom method for filter since we cannot use name property.
    species = filters.CharFilter(method="filter_by_species", label="species")
    author = ...

    @staticmethod
    def filter_by_species(queryset, name, value):
        parts = value.split()  # Splitting by space to separate genus and species
        if len(parts) == 2:
            genus, species = parts
            return queryset.filter(
                speciesproblem__species__genus__iexact=genus,
                speciesproblem__species__species__iexact=species,
            )
        elif len(parts) == 1:
            part = parts[0]
            return queryset.filter(
                Q(speciesproblem__species__genus__icontains=part)
                | Q(speciesproblem__species__species__icontains=part)
            )
        return queryset

    class Meta:
        model = OpenProblem
        fields = ["title", "tags", "gene", "species", "doi"]
