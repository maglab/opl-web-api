from django.contrib import admin
from .models import Gene, GeneProblem, Species, SpeciesProblem, Tag
from import_export.admin import ImportExportModelAdmin
from .resources import (
    TagResource,
    GeneResource,
    GeneProblemResource,
    SpeciesResource,
    SpeciesProblemResource,
)


class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["id", "title"]
    resource_class = TagResource


class GeneAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["gene_name", "gene_symbol"]
    resource_class = GeneResource


class GeneProblemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    autocomplete_fields = ["gene", "open_problem"]
    resource_class = GeneProblemResource


class SpeciesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name", "genus", "species"]
    search_fields = ["name"]
    resource_class = SpeciesResource

    def name(self, obj):
        return obj.name


class SpeciesProblemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    autocomplete_fields = ["species", "open_problem"]
    resource_class = SpeciesProblemResource


admin.site.register(Tag, TagAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(SpeciesProblem, SpeciesProblemAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(GeneProblem, GeneProblemAdmin)
