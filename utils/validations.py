from typing import Union

from open_problems.models.contacts_users import Contact, Organisation
from open_problems.models.references import Journal, Reference


def validate_submitted_reference(title: str, year: str) -> bool:
    """
    Checks whether a reference with the given title and year already exists in the database.

    Args:
        title (str): Title of the reference.
        year (int): Year of the reference publication.

    Returns:
        bool: True if a matching reference exists, False otherwise.
    """
    return Reference.objects.filter(ref_title=title, publish_date=year).exists()


def validate_journal(journal_name: str) -> Union[object, bool]:
    """
    Check whether a journal with the given name exists in the database.

    Args:
        journal_name (str): The name of the journal to validate.

    Returns:
        int or False: The primary key (ID) of the journal if it exists, or False if it doesn't.
    """
    if Journal.objects.filter(journal_name=journal_name).exists():
        journal = Journal.objects.filter(journal_name=journal_name).first()
        return journal
    else:
        return False


def validate_contact(data: dict):
    """
    Check whether the contact is present in the database or not.
    """

    # Start with an empty filter query
    filter_query = {}

    # Add conditions to the filter query based on provided input values
    if "first_name" in data:
        filter_query['first_name__iexact'] = data["first_name"]
    if "last_name" in data:
        filter_query['last_name__iexact'] = data["last_name"]
    if "email" in data:
        filter_query['email__iexact'] = data["email"]


    try:
        # Use the filter method to search for a contact based on the filter query
        contact = Contact.objects.filter(**filter_query).first()

        if contact:
            return True, contact
        else:
            return False, None
    except Contact.DoesNotExist:
        return False, None


def validate_organisation(organisation: str):
    """
    Check whether the organisation is present in the database or not.
    """
    return Organisation.objects.filter(info_title=organisation).exists()


