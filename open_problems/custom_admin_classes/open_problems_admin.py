from django.contrib import admin
from django.shortcuts import redirect, render

from open_problems.forms.forms import CreateRelationForm


# ADMIN ACTIONS FOR FORMING RELATIONSHIPS BETWEEN OPEN PROBLEMS
def set_answers(request, queryset):
    parent_id = request.POST.get("parent_problem")
    parent_query = queryset.get(question_id=parent_id)
    child_query = queryset.all().exclude(question_id=parent_id)[0]
    return parent_query, child_query


# ADMIN ACTIONS FOR SETTING MULTIPLE OPEN PROBLEMS TO ACTIVE OR INACTIVE.
def toggle_active_status(modeladmin, request, queryset):
    for open_problem in queryset:
        open_problem.is_active = not open_problem.is_active
        open_problem.save()
    count = queryset.count()
    message = f"Toggled 'is_active' field for {count} problem(s)."
    modeladmin.message_user(request, message)


toggle_active_status.description = "For setting open problems to active or inactive."


# THE ADMIN CLASS
class OPAdmin(admin.ModelAdmin):
    list_display = ["title", "problem_id", "contact", "is_active", "parent_problem"]
    actions = [toggle_active_status]
    search_fields = ["problem_id", "title"]
    list_filter = ["is_active", "parent_problem"]
