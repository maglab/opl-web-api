from django.contrib import admin
from django.contrib import messages
from open_problems.models.open_problems import ProblemReference
class OpenProblemsReferencesAdmin(admin.ModelAdmin):
    list_filter = ["problem_id"]
    list_display = ["problem_id", "reference_id"]
    search_fields = ["problem_id__title", "reference_id__ref_title"]



