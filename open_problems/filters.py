from django.db.models import Q
from django_filters import FilterSet, filters
from annotations.models import Tag, Gene
from references.models import Reference
from .models import OpenProblem


class MultiValueCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        # value is either a list or an 'empty' value
        values = value or []
        for value in values:
            qs = super(MultiValueCharFilter, self).filter(qs, value)

        return qs.distinct()


class FullNameFilter(filters.CharFilter):
    def filter(self, qs, value):
        values = value or []
        for value in values:
            if value:
                parts = value.split()
                if len(parts) == 2:
                    first_name, last_name = parts
                    qs = qs.filter(
                        Q(contact__first_name__icontains=first_name)
                        & Q(contact__last_name__icontains=last_name)
                    )
                elif len(parts) == 1:
                    part = parts[0]
                    qs = qs.filter(
                        Q(contact__first_name__icontains=part)
                        | Q(contact__last_name__icontains=part)
                    )
        return qs.distinct()


class OpenProblemsFilter(FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = MultiValueCharFilter(field_name="tags__title", lookup_expr="icontains")
    genes = MultiValueCharFilter(
        field_name="genes__gene_symbol", lookup_expr="icontains"
    )
    references = MultiValueCharFilter(
        field_name="references__doi", lookup_expr="icontains"
    )
    # Make custom method for filter since we cannot use name property.
    species = MultiValueCharFilter(
        field_name="species__full_name", label="species", lookup_expr="icontains"
    )
    # For now, we will search the contact table as we do not have any auth users.
    authors = FullNameFilter(label="Author", field_name="contact")

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
        fields = ["title", "tags", "genes", "species", "references", "authors"]
