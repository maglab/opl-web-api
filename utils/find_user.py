from django.db.models import Q

from open_problems.models.contacts_users import Organisation, Contact


def find_user(data: dict) -> object:
    organisation, created = Organisation.objects.get_or_create(
        info_title=data["organisation"]
    )
    contact_query = Q(
        first_name=data["first_name"], last_name=data["last_name"], email=data["email"]
    )
    # Try to find an existing Contact
    contact = Contact.objects.filter(contact_query).first()

    if contact is not None:
        if not contact.organisation:
            contact.organisation = organisation
        # Save the Contact
        contact.save()
        return contact
    else:
        # Create a new Contact and save it
        new_contact = Contact(
            first_name=data["first_name"],
            last_name=data["last_name"],
            organisation=organisation,
        )
        new_contact.save()
        return new_contact
