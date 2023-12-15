from django.contrib import admin

from .models.genes import Gene, GeneProblem
from .models.species import Species
from .models.theory import Theory, TheoryProblem

# Register your models here.


class TheoryProblemAdmin(admin.ModelAdmin):
    list_fields = ["theory_title", "problem_title"]


admin.site.register(Theory)
admin.site.register(TheoryProblem, TheoryProblemAdmin)
admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(GeneProblem)
