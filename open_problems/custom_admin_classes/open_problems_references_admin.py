from django.contrib import admin
from django.contrib import messages
from open_problems.models.open_problems import ProblemReference


class OpenProblemsReferencesAdmin(admin.ModelAdmin):
    list_filter = ["open_problem"]
    list_display = ["open_problem", "reference"]
    search_fields = ["open_problem__title", "reference__title"]
