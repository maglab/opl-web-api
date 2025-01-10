from dataclasses import field

from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from import_export.instance_loaders import ModelInstanceLoader
from .models import OpenProblem, Reference, Tag, Species, Compound, Gene
from categories.models import Category


class OpenProblemResource(resources.ModelResource):
    references = fields.Field(
        attribute="references", widget=ManyToManyWidget(Reference, field="id")
    )
    tags = fields.Field(attribute="tags", widget=ManyToManyWidget(Tag, field="id"))
    species = fields.Field(
        attribute="species", widget=ManyToManyWidget(Species, field="id", separator=",")
    )
    compounds = fields.Field(
        attribute="compounds",
        widget=ManyToManyWidget(Compound, field="id", separator=","),
    )
    genes = fields.Field(
        attribute="genes", widget=ManyToManyWidget(Gene, field="id", separator=",")
    )
    categories = fields.Field(
        attribute="categories", widget=ManyToManyWidget(Category, field="title")
    )

    class Meta:
        model = OpenProblem
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ["problem_id"]
