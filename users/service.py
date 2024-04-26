from users.models import Contact, Organisation, JobField


def get_or_create_contact(data: dict):
    organisation = data.get("organisation", "")
    job_field = data.get("job_field", "")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    email = data.get("email", "")

    if not (first_name and last_name) and not email:
        return None

    organisation_instance = None
    if organisation:
        organisation_instance, _ = Organisation.objects.get_or_create(
            info_title=organisation
        )

    job_field_instance = None
    if job_field:
        job_field_instance, _ = JobField.objects.get_or_create(info_title=job_field)

    contact_instance, created = Contact.objects.get_or_create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        job_field=job_field_instance,
        organisation=organisation_instance,
    )

    return contact_instance
