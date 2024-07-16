from django.contrib import admin, messages
from django.utils.html import format_html, format_html_join
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin

import os

from open_problems.models import (
    Contact,
    OpenProblem,
    SubmittedOpenProblem,
)
from .resources import OpenProblemResource
from core.service import return_url
from core.emails import (
    MailtrapTemplateEmailSender,
    MailtrapConfigurator,
    get_templates,
)

MAILTRAP_TOKEN = os.environ.get("MAILTRAP_API_KEY")


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


class SubmittedProblemsAdmin(admin.ModelAdmin):
    # Filter out many-to-many fields and reverse foreign keys from list_display
    list_display = [
        field.name
        for field in SubmittedOpenProblem._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    actions = ["move_to_open_problems"]
    autocomplete_fields = ["tags", "parent_problem", "genes", "species", "compounds"]
    email_templates = get_templates()
    email_client = MailtrapConfigurator(token=MAILTRAP_TOKEN)

    def set_email_contents(self, request, open_problem):
        template = self.email_templates.get("published")
        if not template:
            raise ValueError("Email template 'published' not found")

        uuid = template.get("uuid")
        email = open_problem.contact.email
        user_name = email.split("@")[0]  # Assuming user_name is the part before '@'

        template_variables = template.get("template_variables", {})
        template_variables.update(
            {
                "contact": user_name,
                "year": timezone.now().year,
                "link": self._build_problem_url(request, open_problem),
            }
        )

        return uuid, user_name, email, template_variables

    @staticmethod
    def _build_problem_url(request, open_problem):
        url_dict = return_url(request)
        scheme = url_dict.get("scheme")
        host = url_dict.get("host")
        if "localhost" in host.lower():
            host = "localhost:3000"
        path = f"open-problems/{open_problem.problem_id}"
        return f"{scheme}://{host}/{path}"

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
                is_active=True,
            )

            # Set the many-to-many fields
            self._set_many_to_many_fields(submitted_problem, open_problem)

            # Send the email
            if submitted_problem.notify_user:
                uuid, user_name, email, template_variables = self.set_email_contents(
                    request, submitted_problem
                )
                self._send_notification_email(email, uuid, template_variables)

        self._notify_admin(request, queryset.count())
        queryset.delete()

    @staticmethod
    def _set_many_to_many_fields(submitted_problem, open_problem):
        open_problem.tags.set(submitted_problem.tags.all())
        open_problem.genes.set(submitted_problem.genes.all())
        open_problem.species.set(submitted_problem.species.all())
        open_problem.compounds.set(submitted_problem.compounds.all())
        open_problem.references.set(submitted_problem.references.all())
        open_problem.save()

    def _send_notification_email(self, email, uuid, template_variables):
        configured_client = self.email_client.configure_client()
        sender = MailtrapTemplateEmailSender(client=configured_client)
        sender.send_email(
            to_email=email, template_uuid=uuid, template_variables=template_variables
        )

    def _notify_admin(self, request, count):
        message = (
            f"{count} submitted problem(s) moved to the official list of open problems and emailed users of "
            f"publication."
        )
        self.message_user(request, message, level=messages.SUCCESS)


admin.site.register(OpenProblem, OpenProblemAdmin)
admin.site.register(SubmittedOpenProblem, SubmittedProblemsAdmin)
admin.site.register(Contact)
