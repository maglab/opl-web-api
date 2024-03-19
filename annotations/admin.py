from django.contrib import admin
from .models.genes import Gene, GeneProblem
from .models.species import Species
from .models.tags import Tag, TagProblem

# Register your models here.


from django.contrib import admin
from .models import TagProblem


class TagAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]


class TagProblemAdmin(admin.ModelAdmin):
    list_display = [
        "tag_title",
        "problem_title",
    ]  # Define the list_display fields correctly
    autocomplete_fields = [
        "tag",
        "open_problem",
    ]  # Use autocomplete_fields for better selection experience

    def tag_title(self, obj):
        return obj.tag.title

    def problem_title(self, obj):
        return obj.open_problem.title


admin.site.register(Tag, TagAdmin)
admin.site.register(TagProblem, TagProblemAdmin)
admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(GeneProblem)
