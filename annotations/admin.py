from django.contrib import admin
from .models import Gene, GeneProblem, Species, SpeciesProblem, Tag


class TagAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]


class GeneAdmin(admin.ModelAdmin):
    search_fields = ["gene_name", "gene_symbol"]


class GeneProblemAdmin(admin.ModelAdmin):
    autocomplete_fields = ["gene", "open_problem"]


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ["name", "genus", "species"]
    search_fields = ["name"]

    def name(self, obj):
        return obj.name


class SpeciesProblemAdmin(admin.ModelAdmin):
    autocomplete_fields = ["species", "open_problem"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(SpeciesProblem, SpeciesProblemAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(GeneProblem, GeneProblemAdmin)
