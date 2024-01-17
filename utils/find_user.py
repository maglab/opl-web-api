from typing import Type

from django.db.models import Q

from open_problems.models.contacts_users import Organisation, Contact
from open_problems.models.open_problems import SubmittedProblems, OpenProblems


def find_user(
    data: dict, open_problem_object: Type[SubmittedProblems | OpenProblems]
) -> object:
    organisation = Organisation.objects.get_or_create(
        info_title=data["organisation"].lower()
    )
    contact_query = Q(
        first_name=data["first_name"], last_name=data["last_name"], email=data["email"]
    )
    contact = Contact.objects.filter(contact_query).first()
    if contact.exists:
        if not contact.organisation:
            contact.organisation = organisation
        return contact
    else:
        contact = Contact(
            first_name=data["first_name"],
            last_name=data["last_name"],
            organisation=organisation,
        )
        return contact
