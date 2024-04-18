from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from .models import OpenProblem, Reference, Tag, Species, Compound, Gene


class OpenProblemResource(resources.ModelResource):
    references = fields.Field(
        attribute="references", widget=ManyToManyWidget(Reference, field="id")
    )  # Assuming 'id' can uniquely identify a Reference
    tags = fields.Field(attribute="tags", widget=ManyToManyWidget(Tag, field="id"))
    species = fields.Field(
        attribute="species", widget=ManyToManyWidget(Species, field="id")
    )
    compounds = fields.Field(
        attribute="compounds", widget=ManyToManyWidget(Compound, field="id")
    )
    genes = fields.Field(attribute="genes", widget=ManyToManyWidget(Gene, field="id"))

    class Meta:
        model = OpenProblem
        skip_unchanged = True
        report_skipped = True
        import_id_fields = [
            "problem_id"
        ]  # Assuming you're using 'problem_id' to identify instances

    def before_import_row(self, row, **kwargs):
        # Clear existing relations
        instance = self.get_instance(instance_loader=None, row=row)
        if instance:
            instance.references.clear()
            instance.tags.clear()
            instance.species.clear()
            instance.compounds.clear()
            instance.genes.clear()

    def save_m2m(self, obj, data, using_transactions, dry_run):
        # Custom save for ManyToMany fields to ensure they are updated as expected
        if not dry_run:
            super(OpenProblemResource, self).save_m2m(
                obj, data, using_transactions, dry_run
            )
