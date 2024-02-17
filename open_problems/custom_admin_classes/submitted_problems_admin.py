from django.contrib import admin
from django.contrib import messages

from open_problems.models.open_problems import (
    OpenProblem,
    SubmittedOpenProblem,
)


class SubmittedProblemsAdmin(admin.ModelAdmin):
    display = [field.name for field in SubmittedOpenProblem._meta.get_fields()] + []
    actions = ["move_to_open_problems"]

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
            )
            # Save the problem
            open_problem.save()
            message = f"{queryset.count()} submitted problem(s) moved to the official list of open problems"
            self.message_user(request, message, level=messages.SUCCESS)
            queryset.delete()
