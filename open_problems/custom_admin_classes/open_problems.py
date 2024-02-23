from django.contrib import admin
from django.shortcuts import redirect, render

from open_problems.forms.forms import CreateRelationForm
from open_problems.models.open_problems import RelatedProblem


# ADMIN ACTIONS FOR FORMING RELATIONSHIPS BETWEEN OPEN PROBLEMS
def set_answers(request, queryset):
    parent_id = request.POST.get("parent_problem")
    parent_query = queryset.get(question_id=parent_id)
    child_query = queryset.all().exclude(question_id=parent_id)[0]
    return parent_query, child_query


def create_relationship_between_problems(modeladmin, request, queryset):
    if len(queryset) < 2:
        modeladmin.message_user(
            request, "Please select at least two questions to create a relationship."
        )
        return

    data = [(query.problem_id, query.title) for query in queryset[:2]]
    form = CreateRelationForm(data=data)
    form_html = form.as_table()

    if "apply" in request.POST:
        parent, child = set_answers(queryset, request.POST.get("parent_problem"))
        RelatedProblem(parent_id=parent, child_id=child).save()
        modeladmin.message_user(
            request, f"Created relationship between: {parent.title} and {child.title}"
        )
        return redirect("admin:questions_questions_changelist")
    else:
        return render(
            request,
            "admin/create_relation.html",
            context={"form": form_html, "query": queryset},
        )


create_relationship_between_problems.short_description = (
    "Create a relationship between two questions"
)


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
    actions = [create_relationship_between_problems, toggle_active_status]
    search_fields = ["problem_id", "title"]
    list_filter = ["is_active", "parent_problem"]
