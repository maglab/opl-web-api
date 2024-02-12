from django.contrib import admin

from posts_comments.models.Post import PostReferences
from references.models import Journal, Reference
from utils.create_reference import create_reference
from utils.validations import validate_journal, validate_submitted_reference


# Action to convert pubmed ids and doi's to
def apply_references(modeladmin, request, queryset):
    failed_conversions = []
    existing_references = []
    successful_conversions = 0

    for reference in queryset:
        reference_type = reference.type
        reference_value = reference.ref
        reference_information = create_reference(
            ref_type=reference_type, value=reference_value
        )

        if reference_information is not None:
            title = reference_information["title"]
            year = reference_information["year"]
            journal = reference_information["journal"]
            doi = reference_information["doi"]
            citation = reference_information["citation"]

            reference_exists = validate_submitted_reference(title, year)
            journal_exists = validate_journal(journal)

            if reference_exists:
                existing_references.append(reference.ref)
            else:
                if journal_exists:
                    journal_instance = journal_exists
                else:
                    new_journal = Journal(journal_name=journal)
                    new_journal.save()
                    journal_instance = new_journal

                reference_object = Reference(
                    ref_title=title,
                    publish_date=year,
                    full_citation=citation,
                    journal_id=journal_instance,
                    doi=doi,
                )
                reference_object.save()
                PostReferences(
                    reference_id=reference_object, submission_id=reference.submission_id
                ).save()

            successful_conversions += 1  # Increment successful conversion count

        else:
            failed_conversions.append(reference.ref)

        reference.delete()  # Delete the reference after processing

    failed_string = ", ".join(failed_conversions)
    existing_string = ", ".join(existing_references)
    message = f"{successful_conversions} successfully converted and saved as references. \
        {len(existing_references)} references already existed: {existing_string}. \
        {len(failed_conversions)} failed to convert: {failed_string}"
    modeladmin.message_user(request, message)


apply_references.short_description = "Convert and Save References"

apply_references.description = (
    "Extract reference information from user submitted DOIs and PUBMED Ids - "
)


# CUSTOM CLASS
class SubmittedReferencesAdmin(admin.ModelAdmin):
    list_display = [
        "reference_id",
        "type",
        "ref",
        "submission_id",
        "submission_full_text",
    ]
    actions = [apply_references]

    def submission_full_text(self, obj):  # Return the full text of the submission?
        return obj.submission_id.full_text
