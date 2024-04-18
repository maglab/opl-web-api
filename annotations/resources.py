from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Tag, Gene, Species


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag


class GeneResource(resources.ModelResource):
    species = fields.Field(
        column_name="species",
        attribute="species",
        widget=ForeignKeyWidget(Species, field="full_name"),
    )

    class Meta:
        model = Gene


class SpeciesResource(resources.ModelResource):
    class Meta:
        model = Species
