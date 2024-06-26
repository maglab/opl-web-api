from django.contrib import admin, messages
from django.utils.html import format_html, format_html_join
from import_export.admin import ImportExportModelAdmin

from open_problems.models import (
    Contact,
    OpenProblem,
    SubmittedOpenProblem,
)
from .resources import OpenProblemResource


class OpenProblemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = OpenProblemResource
    list_display = ["title", "problem_id", "contact", "is_active", "parent_problem"]
    actions = ["toggle_active_status"]
    search_fields = ["problem_id", "title"]
    list_filter = ["is_active", "parent_problem"]
    autocomplete_fields = ["tags", "parent_problem", "genes", "species", "compounds"]
    readonly_fields = ("list_children",)

    @admin.action(description="Set active or inactive")
    def toggle_active_status(self, request, queryset):
        for open_problem in queryset:
            open_problem.is_active = not open_problem.is_active
            open_problem.save()
        count = queryset.count()
        message = f"Toggled 'is_active' field for {count} problem(s)."
        self.message_user(message)

    def list_children(self, obj):
        children = obj.children.all()
        if children:
            return format_html(
                "<ul>{}</ul>",
                format_html_join(
                    "\n",
                    "<li><a href='{}'>{}</a></li>",
                    (
                        (
                            f"/api/admin/{obj._meta.app_label}/{obj._meta.model_name}/{child.pk}/change/",
                            child,
                        )
                        for child in children
                    ),
                ),
            )
        return "No children"

    list_children.short_description = "Child Problems"


# Registering models to admin without class created.
class SubmittedProblemsAdmin(admin.ModelAdmin):
    display = [field.name for field in SubmittedOpenProblem._meta.get_fields()] + []
    actions = ["move_to_open_problems"]
    autocomplete_fields = ["tags", "parent_problem", "genes", "species", "compounds"]

    @admin.action(
        description="Move submitted problem(s) to the official list of open problems"
    )
    def move_to_open_problems(self, request, queryset):
        for submitted_problem in queryset:
            open_problem = OpenProblem.objects.create(
                title=submitted_problem.title,
                description=submitted_problem.description,
                parent_problem=submitted_problem.parent_problem,
                contact=submitted_problem.contact,
                references=submitted_problem.references,
                tags=submitted_problem.tags,
                genes=submitted_problem.genes,
                species=submitted_problem.species,
                compounds=submitted_problem.compounds,
                is_active=True,
            )
            # Save the problem
            open_problem.save()
            message = f"{queryset.count()} submitted problem(s) moved to the official list of open problems"
            self.message_user(request, message, level=messages.SUCCESS)
            queryset.delete()


admin.site.register(OpenProblem, OpenProblemAdmin)
admin.site.register(SubmittedOpenProblem, SubmittedProblemsAdmin)
admin.site.register(Contact)
