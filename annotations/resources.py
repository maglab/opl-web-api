from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Tag, Gene, GeneProblem, Species, SpeciesProblem
from open_problems.models import OpenProblem


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class GeneResource(resources.ModelResource):
    class Meta:
        model = Gene


class GeneProblemResource(resources.ModelResource):
    open_problem = fields.Field(
        column_name="open_problem",
        attribute="open_problem",
        widget=ForeignKeyWidget(OpenProblem, "problem_id"),
    )
    gene = fields.Field(
        column_name="gene", attribute="gene", widget=ForeignKeyWidget(Gene, "id")
    )

    class Meta:
        model = GeneProblem
        # Removed import_id_fields to stop treating any field combination as unique
        import_id_fields = ["open_problem", "gene"]
        skip_unchanged = True
        report_skipped = True


class SpeciesResource(resources.ModelResource):
    class Meta:
        model = Species


class SpeciesProblemResource(resources.ModelResource):
    open_problem = fields.Field(
        column_name="open_problem",
        attribute="open_problem",
        widget=ForeignKeyWidget(OpenProblem, "problem_id"),
    )
    species = fields.Field(
        column_name="species",
        attribute="species",
        widget=ForeignKeyWidget(Species, "id"),
    )

    class Meta:
        model = SpeciesProblem
        import_id_fields = ["open_problem", "species"]
        report_skipped = True
