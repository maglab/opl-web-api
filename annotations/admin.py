from django.contrib import admin
from .models import Gene, Species, Tag, Compound
from import_export.admin import ImportExportModelAdmin
from .resources import (
    TagResource,
    GeneResource,
    SpeciesResource,
)


class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["id", "title"]
    resource_class = TagResource


class GeneAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["gene_name", "gene_symbol"]
    resource_class = GeneResource


class SpeciesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["full_name", "genus", "species"]
    search_fields = ["full_name"]
    resource_class = SpeciesResource

    def name(self, obj):
        return obj.name


class CompoundAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "chembl_id", "pubchem_id"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(Compound, CompoundAdmin)
