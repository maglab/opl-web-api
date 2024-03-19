from django.contrib import admin
from .models.genes import Gene, GeneProblem
from .models.species import Species
from .models.tags import Tag, TagProblem

# Register your models here.


class SubjectProblemAdmin(admin.ModelAdmin):
    list_fields = ["theory_title", "problem_title"]


admin.site.register(Tag)
admin.site.register(TagProblem, SubjectProblemAdmin)
admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(GeneProblem)
