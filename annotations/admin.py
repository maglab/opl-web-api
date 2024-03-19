from .models import Tag, Gene, GeneProblem, Species
from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(GeneProblem)
