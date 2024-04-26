from django.contrib import admin, messages
from .models import Gene, Species, Tag, Compound
from import_export.admin import ImportExportModelAdmin
from .resources import (
    TagResource,
    GeneResource,
    SpeciesResource,
)


class VerifyAdminMixin:
    actions = ["make_verified", "make_unverified"]

    def make_verified(self, request, queryset):
        updated_count = queryset.update(verified=True)
        if updated_count == 1:
            message_bit = "1 record was"
        else:
            message_bit = f"{updated_count} records were"
        self.message_user(
            request, f"{message_bit} successfully marked as verified.", messages.SUCCESS
        )

    make_verified.short_description = "Mark selected items as verified"

    def make_unverified(self, request, queryset):
        updated_count = queryset.update(verified=False)
        if updated_count == 1:
            message_bit = "1 record was"
        else:
            message_bit = f"{updated_count} records were"
        self.message_user(
            request,
            f"{message_bit} successfully marked as unverified.",
            messages.SUCCESS,
        )

    make_unverified.short_description = "Mark selected items as unverified"


class TagAdmin(ImportExportModelAdmin, VerifyAdminMixin, admin.ModelAdmin):
    search_fields = ["id", "title"]
    resource_class = TagResource


class GeneAdmin(ImportExportModelAdmin, VerifyAdminMixin, admin.ModelAdmin):
    search_fields = ["gene_name", "gene_symbol"]
    resource_class = GeneResource


class SpeciesAdmin(ImportExportModelAdmin, VerifyAdminMixin, admin.ModelAdmin):
    list_display = ["full_name", "genus", "species"]
    search_fields = ["full_name"]
    resource_class = SpeciesResource

    def name(self, obj):
        return obj.name


class CompoundAdmin(ImportExportModelAdmin, VerifyAdminMixin, admin.ModelAdmin):
    list_display = ["id", "name", "chembl_id", "pubchem_id"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(Compound, CompoundAdmin)
