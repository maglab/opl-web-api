from django.contrib import admin
from .models.genes import Gene, GeneProblem
from .models.species import Species
from .models.subjects import Subject, SubjectProblem

# Register your models here.


class SubjectProblemAdmin(admin.ModelAdmin):
    list_fields = ["theory_title", "problem_title"]


admin.site.register(Subject)
admin.site.register(SubjectProblem, SubjectProblemAdmin)
admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(GeneProblem)
