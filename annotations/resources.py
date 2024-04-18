from import_export import resources
from .models import Tag, Gene, Species


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class GeneResource(resources.ModelResource):
    class Meta:
        model = Gene


class SpeciesResource(resources.ModelResource):
    class Meta:
        model = Species
