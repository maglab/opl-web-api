from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.instance_loaders import ModelInstanceLoader
from .models import OpenProblem, Reference, Tag, Species, Compound, Gene


class OpenProblemResource(resources.ModelResource):
    references = fields.Field(
        attribute="references", widget=ManyToManyWidget(Reference, field="id")
    )  # Assuming 'id' can uniquely identify a Reference
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

    class Meta:
        model = OpenProblem
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ["problem_id"]
