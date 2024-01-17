import json

from django.contrib import admin
from django.contrib import messages

from open_problems.models.open_problems import (
    OpenProblems,
    ProblemReference,
    SubmittedProblems,
)
from open_problems.models.references import Journal, Reference
from utils.find_user import find_user


class SubmittedProblemsAdmin(admin.ModelAdmin):
    display = [field.name for field in SubmittedProblems._meta.get_fields()] + []
    actions = ["move_to_open_problems"]

    def save_references(self, references):
        references_json = json.loads(references)
        references_list = []

        for key, reference_info in references_json.items():
            title = reference_info.get("title", "")
            year = reference_info.get("year", "")
            journal_name = reference_info.get("journal", "")
            doi = reference_info.get("doi", "")
            citation = reference_info.get("citation", "")

            # Handle the journal
            journal, created = Journal.objects.get_or_create(journal_name=journal_name)

            if created:
                journal.save()

            reference, created = Reference.objects.get_or_create(
                ref_title=title,
                publish_date=year,
                defaults={
                    "doi": doi,
                    "full_citation": citation,
                    "journal_id": journal,
                },
            )

            if not created:
                # Reference already exists, so we update the fields
                reference.doi = doi
                reference.citation = citation
                reference.save()

            references_list.append(reference)

        return references_list

    @admin.action(
        description="Move submitted problem(s) to the official list of open problems"
    )
    def move_to_open_problems(self, request, queryset):
        for submitted_problem in queryset:
            open_problem = OpenProblems.objects.create(
                title=submitted_problem.title,
                description=submitted_problem.description,
                parent_problem=submitted_problem.parent_problem,
            )

            # Check the contact details
            contact_data = {
                "first_name": submitted_problem.first_name.capitalize(),
                "last_name": submitted_problem.last_name.capitalize(),
                "email": submitted_problem.email,
                "organisation": submitted_problem.organisation.capitalize(),
            }
            if (
                contact_data["first_name"]
                and contact_data["last_name"]
                or contact_data["email"]
            ):

                contact = find_user(
                    data=contact_data, open_problem_object=submitted_problem
                )
                open_problem.contact = contact

            # Set the contact to none if no contact details are provided
            else:
                open_problem.contact = None

            # Save the problem
            open_problem.save()

            # Check for references and save accordingly. If there are no references save the problem. If there are
            # references, save the problem and save the problem with the references using ProblemReference model
            references = submitted_problem.references
            if references:
                references_list = self.save_references(references)
                for reference in references_list:
                    open_problem_reference = ProblemReference.objects.create(
                        problem_id=open_problem, reference_id=reference
                    )
                    open_problem_reference.save()

        message = f"{queryset.count()} submitted problem(s) moved to the official list of open problems"
        self.message_user(request, message, level=messages.SUCCESS)
        queryset.delete()
